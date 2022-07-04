from typing import Callable, Optional, Tuple, Iterable
import functools
import torch
import attr

from fed_reconstruct import algo

DatasetSplitFn = Callable[[torch.Dataset, torch.tenosr],
                          Tuple[torch.Datasest, torch.Dataset]]


def simple_dataset_split(client_dataset: torch.Dataset,
                         round_num: torch.Tensor) -> Tuple[torch.Dataset,
                                                           torch.Dataset]:
    return client_dataset, client_dataset

def build_dataset_split(recon_epochs_max: int = 1,
                        recon_epochs_constant: bool = True,
                        recon_steps_max: Optional[int] = None,
                        post_recon_epochs: int = 1,
                        post_recon_steps_max: Optional[int] = None,
                        split_dataset: bool = False) -> DatasetSplitFn:

    def recon_condition(i, entry): return torch.tensor(
        i) % torch.tensor(2) == 0
    def post_recon_condition(i, entry): return torch.tensor(
        i) % torch.tensor(2) > 0

    def get_entry(i, entry): return entry

    def dataset_split(clinet_dataset, round_num: torch.Tensor):
        if split_dataset:
            recon_dataset = clinet_dataset.enumerate().filter(
                recon_condition).map(get_entry)
            post_recon_dataset = clinet_dataset.enumerate().filter(
                post_recon_condition).map(get_entry)

        else:
            recon_dataset = clinet_dataset
            post_recon_dataset = clinet_dataset

        # Number of reconstruction epochs is exactly recon_epochs_max if
        # recon_epochs_constant is True, and min(round_num, recon_epochs_max)
        # if not
        num_recon_epochs = recon_epochs_max
        if not recon_epochs_constant:
            num_recon_epochs = torch.minimum(round_num, recon_epochs_max)

        # Apply `num_recon_epochs`` before limiting to a maximum number of
        # batches if needed.
        recon_dataset = recon_dataset.repeat(num_recon_epochs)
        if recon_steps_max is not None:
            recon_dataset = recon_dataset.take(recon_steps_max)

        # Do the same for post-reconstruction.
        post_recon_dataset = post_recon_dataset.repeat(post_recon_epochs)
        if post_recon_steps_max is not None:
            post_recon_dataset = post_recon_dataset.take(post_recon_steps_max)

        return recon_dataset, post_recon_dataset
    return dataset_split

def get_global_variables(model: algo.ReconstructionModel) -> torch.Tensor:
    return torch.cat([model.global_trainable_variables,
                      model.global_non_trainable_variables])

def get_local_variables(model: algo.ReconstructionModel) -> torch.Tensor:
    return torch.cat([model.local_trainable_variables,
                      model.local_non_trainable_variables]) 

def has_only_gloabal_variables(model: algo.ReconstructionModel) -> bool:
    return len(model.global_trainable_variables) == 0 and \
        len(model.global_non_trainable_variables) > 0     

@attr.s(eq=False, frozen=True)
class ServerState(object):
    model = attr.ib()
    optimizer_state = attr.ib()
    aggregator_state = attr.ib()

@attr.s(eq=False, frozen=True)
class ClientOutput(object):
    weights_delta = attr.ib()
    client_weight = attr.ib() 
    model_output = attr.ib()

def map_structure(func: Callable, *args):
    return tuple(map(func, *args))
    
def create_optimizer_vars(
    model: algo.ReconstructionModel,
    optimizer: torch.optim.Optimizer,
) -> Iterable[torch.Tensor]:
    delta = map_structure(torch.zeros_like,get_global_variables(model).trainable)
    grads_and_vars = map_structure(lambda x,v: (-1.0 * x, v), torch.flatten(delta))
    optimizer.apply_gradients(grads_and_vars, name="server_update")
    return optimizer.variables()


def zero_all_if_any_non_finite(structure):
    
    flat =  torch.flatten(structure) 
    if not flat:
        return (structure, torch.tensor(0)) 
  
    flat_bools = [False if torch.isfinite(t) else True for t in flat]
    all_finite = functools.reduce(torch.logical_and, flat_bools)
    if all_finite:
        return (structure, torch.tensor(0))
    else:
        return(map_structure(lambda x: torch.zeros_like(x), structure),
                torch.tensor(1))

