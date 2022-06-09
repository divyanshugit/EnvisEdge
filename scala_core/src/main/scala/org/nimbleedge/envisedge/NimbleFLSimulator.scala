package org.nimbleedge.envisedge

import akka.actor.typed.ActorSystem

object NimbleFLSimulator {
	def main(args: Array[String]): Unit = {
		ActorSystem[SimulatorSupervisor.Command](SimulatorSupervisor(), "nimble-fl-simulator")
	}
}