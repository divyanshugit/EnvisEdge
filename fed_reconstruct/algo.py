from utilities import build_dataset_split
import abc
import attr

@attr.s(eq=False, frozen=True, slots=True)
class BatchOutput(object):
    predictions = attr.ib()
    labels = attr.ib()
    num_examples = attr.ib()
    
class ReconstructionModel:
    @abc.abstractproperty
    def global_trainable_variables(self):
        pass
    @abc.abstractproperty
    def global_non_trainable_variables(self):
        pass

    @abc.abstractproperty
    def local_trainable_variables(self):
        pass

    @abc.abstractproperty
    def local_non_trainable_variables(self):
        pass
    @abc.abstractmethod
    def forward_pass(self, batch_input, training=True):
        pass