package org.nimbleedge.envisedge.models

import scala.collection.mutable.{Map => MutableMap}
/*
class contains history of each trainer 
gets updated after every FlCycle

Trainer-Id / Device-Id will remain same throughout all FL Cycles
*/
case class TrainerHistory (

    /*
    FL cycle in which the device participated
    */
    numParticipatedFLCycle : Int,

    /*
    FL cycle in which the device model was considered for Aggregation
    */
    numCompletedFLCycle : Int,

    /*
    modelMerged contains history that which model version of trainer merged with which version of global model
    Map[TrainerModelID/Version, GlobalModelId]

    This will help to keep track either the global model quality got depleted because of
    that particular trainer model (can be because of biasness, overfitting etc)

    Will make us take better decision for Sampling next time
    */
    modelMerged : MutableMap[String,String],

    // TODO
    // Add more parameters here

)