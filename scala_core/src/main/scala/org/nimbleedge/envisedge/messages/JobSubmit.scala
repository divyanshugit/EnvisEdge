package org.nimbleedge.envisedge.messages

// This class will contain fields which are common to all type of Job Submit Message

case class JobSubmitBasic (
    /*
        ? ask what is stores
    */
    __type__ : String,
    // job types define what type of job it is (sampling, aggregating etc)
    job_type : String,
    // Sender Id who is sending the job submit message (? ask producer or which id)
    sender_id : String,
    // Receiver Id (? clarify what it means)
    receiver_id : String,

)