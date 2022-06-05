package org.nimbleedge.envisedge

import org.nimbleedge.envisedge.models.OrchestratorIdentifier

object ConfigManager {
    val DEFAULT_TASK_ID = "DEFAULT"

    var maxClientsInAgg : Int = 2000
    var samplingPolicy : String = "default"

    var aggregatorS3ProbeIntervalSec = 10

    def getOrcId(taskId : String) : OrchestratorIdentifier = {
        return OrchestratorIdentifier("Orc-" + taskId)
    }
}
