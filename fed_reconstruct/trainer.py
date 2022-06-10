from curses.panel import bottom_panel
import functools
from ntpath import join
from typing import Callable, List, Optional

from absl import logging
import torch

from fed_reconstruct import algo
from fed_reconstruct import utilities

ClientWeightFn = Callable[..., float]
ModelFn = Callable[[], algo.ReconstructionModel]
OptimizerFn = Callable[..., torch.optim.Optimizer]

def build_server_init(
    model_fn: ModelFn, server_optimizer: OptimizerFn,
    model_weights_type, server_state_type,aggregator_state_type
)->Callable[[], None]:
  """Builds the server initialization function.

  Args:
    model_fn: A function that returns the model.
    server_optimizer: A function that returns the optimizer.

  Returns:
    A function that initializes the server.
  """
  def server_init():
    """Initializes the server."""
    logging.info('Initializing server.')
    round_num = torch.tensor(1, dtype=torch.int64)
    model = model_fn()
    optimizer = server_optimizer()
    
    server_optimizer_vars = utilities.create_optimizer_vars(
        model, server_optimizer)

    return utilities.get_global_variables(
        model),server_optimizer_vars, round_num

    trainable_variables = model_weights_type.trainable
  return server_init

def build_client_update_fn(
    model_fn: ModelFn,
    *,  # Callers should use keyword args for below.
    loss_fn: LossFn,
    metrics_fn: Optional[MetricsFn],
    model_weights_type,
    client_optimizer_fn: OptimizerFn,
    reconstruction_optimizer_fn: OptimizerFn,
    dataset_split_fn: utilities.DatasetSplitFn,
    evaluate_reconstruction: bool,
    jointly_train_variables: bool,
    client_weight_fn: Optional[ClientWeightFn] = None,
):
    """Builds the client update function.  This function is called by the
    client to update the model."""
    def client_update(model, metrics, batch_loss_fn, dataset, initial_weights,
                        client_optimizer,reconstruction_optimizer,round_num):
        """Updates the model."""

        global_model_weights = utilities.get_global_variables(model)
        local_model_weights = utilities.get_local_variables(model)
        utilities.map_structure(lambda a,b: a.assign(b), global_model_weights,
                                initial_weights)
        def train_step(batch_input,optimizer):
            """Runs a single training step."""
            with torch.enable_grad():
                batch_loss = batch_loss_fn(model, batch_input)
                batch_loss.backward()
                if client_weight_fn is not None:
                    batch_loss *= client_weight_fn(batch_input)
                else:
                    batch_loss *= 1.0
                client_optimizer.step()
                client_optimizer.zero_grad()
                if jointly_train_variables:
                    optimizer.step()
                    optimizer.zero_grad()
            return batch_loss.item()
        def recons_reduce(epochs,dataset):
            for epoch in range(epochs):
                dataset_split = dataset_split_fn(dataset)
                for batch_input in dataset_split:
                    score = model(batch_input)
                    recon_batch_loss = train_step(batch_input,client_optimizer)
                    if evaluate_reconstruction:
                        train_step(batch_input,reconstruction_optimizer)
                    if metrics_fn is not None:
                        metrics = metrics_fn(model, batch_input, metrics)
                    if round_num % 100 == 0:
                        logging.info('Round %d, batch loss %f', round_num,
                                        batch_loss)
                    round_num += 1

                return 

    def train_reduce(epochs,dataset):
        for epoch in range(epochs):
            dataset_split = dataset_split_fn(dataset)
            for batch_input in dataset_split:
                train_batch_loss = train_step(batch_input,client_optimizer)
                if evaluate_reconstruction:
                    train_step(batch_input,client_optimizer)
                if metrics_fn is not None:
                    metrics = metrics_fn(model, batch_input, metrics)
                if round_num % 100 == 0:
                    logging.info('Round %d, batch loss %f', round_num,
                                    batch_loss)
                round_num += 1

        recon_dataset, post_recon_dataset = dataset_split_fn(dataset,round_num)

        if local_model_weights.trainable:
            recon_dataset.reduce(
                initital_state=torch.tensor(0), reduce_func=reconstruction_reduce_fn
            )
        
    return client_update



























        # for epoch in range(epochs):
        #     for batch, (data, target) in enumerate(dataset):
        #         # Obtaining the cuda parameters
        #         device = torch.device('cuda' if torch.cuda.is_available() 
        #                             else cpu)

        #         data = data.to(device=device)
        #         target = target.to(device=device)
        #         # Forward propagation
        #         score = model(data)
        #         loss = train_step(data,reconstruction_optimizer)
        #         loss = batch_loss_fn(score, target)
        #         reconstruction_optimizer.zero_grad()
        #         loss.backward()
        #         reconstruction_optimizer.step()


        # def train_reduce_function(epochs, dataset):
        #     for epoch in range(epochs):
        #         for batch, (data, target) in enumerate(dataset):
        #             if jointly_train_variables:
        #                 all_train_variables = (
        #                     global_model_weights.trainable + local_model_weights.trainable
        #                 )

        #             else: 
        #                 all_train_variables = global_model_weights.trainable            

        #             # Obtaining the cuda parameters
        #             device = torch.device('cuda' if torch.cuda.is_available() 
        #                                 else cpu)

        #             data = data.to(device=device)
        #             target = target.to(device=device)
        #             # Forward propagation
        #             score = model(data)
        #             loss = batch_loss_fn(score, target)
        #             client_optimizer.zero_grad()
        #             loss.backward()
        #             client_optimizer.step()


