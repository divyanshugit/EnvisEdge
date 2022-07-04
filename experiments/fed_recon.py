"""
Implementation of Federated Reconstruction(FedRecon) Algorithm

At a high level, local variables are reconstructed via training on client
devices at the begining of each round and never sent to the server. Each
client's local variables are then used to update the global variables. Global 
variables deltas are aggregated normally on the server as in Federated Averaging
and sent to new clients at beginning of next round.
"""
# Federated Reconstruction Process
import logging
from typing import Dict
from grpc import server

import torch
# from fedrec.user_modules.envis_base_module import EnvisBase
# from fedrec.user_modules.envis_preprocessor import EnvisPreProcessor
# from fedrec.utilities import registry
# from fl_strategies.fed_avg import FedAvg

from fed_reconstruct import utilities


class BuildFedReconServer():
    def __init__(self, model, server_optimizer, server_state,
            server_optimizer_vars, round_num, aggregator_state):
        super(BuildFedReconServer, self).__init__()
        self.model = model
        self.server_optimizer = server_optimizer
        self.server_optimizer_vars = server_optimizer_vars
        self.server_state = server_state
        self.round_num = round_num
        self.aggregator_state = aggregator_state
        
        
    def server_init(self):
        """Initializes the server."""

        logging.info('Initializing server.')
        round_num = torch.tensor(1, dtype=torch.int64)
        model = self.model
        server_optimizer = self.server_optimizer

        server_optimizer_vars = utilities.create_optimizer_vars(
            model, server_optimizer)

        return utilities.get_global_variables(
            model),server_optimizer_vars, round_num

        # trainable_variables = model_weights_type.trainable
        # return server_init

    def server_update(self):
        server_state = self.server_state
        global_model_weights = utilities.get_global_variables(self.model)
        #Intialize the model with the current state:

        weights_delta = utilities.map_structure(lambda a,b: a.assign(b),
                            (global_model_weights, self.server_optimizer_vars),
                            (server_state.model, server_state.optimizer_state))
        weights_delta, has_non_finite_weight = (
            utilities.zero_all_if_any_non_finite(weights_delta))

        if has_non_finite_weight > 0:
            server_state = server_state
            model = global_model_weights
            optimizer_state = self.server_optimizer_vars
            round_num = server_state.round_num + 1
            aggregator_state=self.aggregator_state
            
            return server_state, model, optimizer_state, round_num, aggregator_state
        
        grads_and_var = utilities.map_structure(lambda x,v: (-1.0*x,v),
                            torch.flatten(weights_delta),
                            torch.flatten(global_model_weights.trainable))

        self.server_optimizer.apply_gradients(grads_and_var, name="server_update")
        server_state = server_state
        model = global_model_weights
        optimizer_state = self.server_optimizer_vars
        round_num = server_state.round_num + 1
        aggregator_state=self.aggregator_state

        return server_state, model, optimizer_state, round_num, aggregator_state
            


        # Update the model:

class ClientUpdate():
    def __init__(self, batch_input, optimizer,initial_weights,
                batch_loss_fn,client_weight_fn,
                client_optimizeer,jointly_train_variables,):
        super(ClientUpdate, self).__init__()
        self.batch_input = batch_input
        self.optimizer = optimizer
        self.initial_weights = initial_weights
        self.batch_loss_fn = batch_loss_fn
        self.client_weight_fn = client_weight_fn
        self.client_optimizer = client_optimizeer
        self.jointly_train_variables = jointly_train_variables


    def client_update(self):
        global_model_weights = utilities.get_global_variables(self.model)
        local_model_weights = utilities.get_local_variables(self.model)
        utilities.map_structure(lambda a,b: a.assign(b), global_model_weights,
                                self.initial_weights)

        # def train_step(self):
        #     """Runs a single training step."""
        #     with torch.enable_grad():
        #         batch_loss = self.batch_loss_fn(self.model, self.batch_input)
        #         batch_loss.backward()

        #         if self.client_weight_fn() is not None:
        #             batch_loss *= self.client_weight_fn(self.batch_input)
        #         else:
        #             batch_loss *= 1.0
        #         self.client_optimizer.step()
        #         self.client_optimizer.zero_grad()
        #         if self.jointly_train_variables:
        #             self.optimizer.step()
        #             self.optimizer.zero_grad()
        #     return batch_loss.item()                        

class Reconstruct():
    def __init__():
        pass

