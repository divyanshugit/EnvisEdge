package org.nimbleedge.envisedge.messages

import javax.annotation.processing.Messager
import scala.collection.Map

// This class will contain fields which are common to all type of Job Submit Message

case class JobSubmitMessage (
    __type__ : String,
    __data__ : JobSubmitMessageData
)

case class JobSubmitMessageData (
    job_args : List[String],
    job_kwargs : Object,
    workerstate : WorkerState,
    job_type : String,
    senderid : String,
    receiverid : String
)

case class WorkerState (
    __type__ : String,
    __data__ : WorkerStateData
)

case class WorkerStateData (
    worker_index : String,
    round_index : Int,
    state_dict : StateDict,
    storage : String,
    model_prepoc : ModelPreproc,
    local_sample_number : Int,
    local_training_steps : Int
)

case class StateDict (
    model : StateDictModel,
    worker_state : SubWorkerState,
    step : Int
)

case class StateDictModel (
    __type__ : String,
    __data__ : StateDictModelData
)

case class StateDictModelData (
    storage : String
)

case class SubWorkerState (
    model : SubWorkerStateModel,
    in_neighbours : Map[String, Neighbour],
    out_neighbours : Map[String, Neighbour]
)

case class SubWorkerStateModel (
    __type__ : String,
    __data__ : SubWorkerStateModelData
)

case class SubWorkerStateModelData (
    class_ref_name : String,
    state : SubWorkerStateModelDataState,
)

case class SubWorkerStateModelDataState (
    __type__ : String,
    __data__ : SubWorkerStateModelDataStateData
)

case class SubWorkerStateModelDataStateData (
    tensor_path : String
)

case class Neighbour (
    __type__ : String,
    __data__ : NeighbourData
)

case class NeighbourData (
    worker_index : String,
    last_sync : Int,
    sample_num : Int,
    model_state : NeighbourDataModelState
)

case class NeighbourDataModelState (
    __type__ : String,
    __data__ : NeighbourDataModelStateData
)

case class NeighbourDataModelStateData (
    storage : String
)

case class ModelPreproc (
    __type__ : String,
    __data__ : ModelPreprocData
)

case class ModelPreprocData (
    proc_name : String,
    client_id : String,
    dataset_config : DatasetConfig
)

case class DatasetConfig (
    name : String,
    data_dir : String,
    splits : List[String],
    normalize : List[Float]
)