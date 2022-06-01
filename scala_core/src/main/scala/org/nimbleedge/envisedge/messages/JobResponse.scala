package org.nimbleedge.envisedge.messages

// response message that scala gets from python
// This message contains basic fields of Job Response Message

case class LinearWeightResultJobResponse (
    __type__ : String,
    __data__Storage : String
)

case class LinearBiasResultJobResponse (
    __type__ : String,
    __data__Storage : String
)

case class ResultJobResponse (
    linearWeight : LinearWeightResultJobResponse,
    linearBias : LinearBiasResultJobResponse
)

case class DataJobResponse (
    job_type : String,
    sender_id : Int,
    receiver_id : Int,
    results : ResultJobResponse
)

case class JobResponseBasic (
    __type__ : String,
    __data__ : DataJobResponse
)