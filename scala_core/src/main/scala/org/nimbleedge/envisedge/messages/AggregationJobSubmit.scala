package org.nimbleedge.envisedge.messages

// job message that scala sends to python for doing different tasks
// general prototype of job-submit message
// will change depending on type of job
case class WorkerState_Model_Data_JobSubmit (
    class_ref_name : String,
    state_type : String,
    state_data_tensor_path : String
)

case class State_Dict_JobSubmit (
    model_type : String,
    model_data_storage : String,
    worker_state_model_type : String,
    worker_state_model_data : WorkerState_Model_Data_JobSubmit,
    step : Int
)

case class DataSetConfig_Model_Prepoc_JobSubmit (
    name : String,
    data_dir : String,
    splits : List[String],
    normalize : List[Float]
)

case class Data_Model_Prepoc_JobSubmit (
    proc_name : String,
    client_id : Int,
    dataset_config : DataSetConfig_Model_Prepoc_JobSubmit
)

case class Model_Prepoc_JobSubmit (
    __type__ : String,
    __data__ : Data_Model_Prepoc_JobSubmit
)

case class WorkerState_Data_JobSubmit (
    worker_index : Int,
    round_index : Int,
    state_dict : State_Dict_JobSubmit,
    storage : String,
    model_prepoc : Model_Prepoc_JobSubmit,
    local_sample_number : Int,
    local_training_steps : Int
)

case class WorkerState_JobSubmit(
    __type__ : String,
    __data__ : WorkerState_Data_JobSubmit
)

case class Data_JobSubmit (
    job_type : String,
    job_args : List[Int],
    job_kwargs : List[Int],
    sender_id :  Int,
    receiver_id : Int,
    workerstate : WorkerState_JobSubmit
)

case class JobSubmit (
    __type__ : String,
    __data__ : Data_JobSubmit
)