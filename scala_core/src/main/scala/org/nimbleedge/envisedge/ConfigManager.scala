package org.nimbleedge.envisedge

import org.nimbleedge.envisedge.models.OrchestratorIdentifier

object ConfigManager {
    val DEFAULT_TASK_ID = "DEFAULT"
    val AGGREGATOR_REQUEST_TOPIC = "job-request-aggregator"
    val AGGREGATOR_RESPONSE_TOPIC = "job-response-aggregator"
    val FLSYS_RESPONSE_TOPIC = "fl-response"
    val FLSYS_REQUEST_TOPIC = "fl-request"

    var maxClientsInAgg : Int = 2000
    var samplingPolicy : String = "default"

    val aggConsumerTopics: Vector[String] = Vector(AGGREGATOR_RESPONSE_TOPIC)
    val flSysConsumerTopics: Vector[String] = Vector(FLSYS_REQUEST_TOPIC)

    var aggregatorS3ProbeIntervalSec = 10

    def getOrcId(taskId : String) : OrchestratorIdentifier = {
        return OrchestratorIdentifier("Orc-" + taskId)
    }
}
