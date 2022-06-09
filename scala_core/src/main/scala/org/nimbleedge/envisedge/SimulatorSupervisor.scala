package org.nimbleedge.envisedge

import akka.actor.typed.Behavior
import akka.actor.typed.Signal
import akka.actor.typed.PostStop
import akka.actor.typed.scaladsl.AbstractBehavior
import akka.actor.typed.scaladsl.ActorContext
import akka.actor.typed.scaladsl.Behaviors

object SimulatorSupervisor {
	// Update this to manager to other entities
	def apply(): Behavior[Command] =
		Behaviors.setup[Command](new SimulatorSupervisor(_))

	sealed trait Command

	case class FLSystemManagerTerminated() extends Command
}

class SimulatorSupervisor(context: ActorContext[SimulatorSupervisor.Command]) extends AbstractBehavior[SimulatorSupervisor.Command](context) {
	import SimulatorSupervisor._
	context.log.info("Simulator Supervisor started")

	val actorRef = context.spawn(FLSystemManager(), "FLSystemManager")
	context.watchWith(actorRef, FLSystemManagerTerminated())

	override def onMessage(msg: Command): Behavior[Command] = {
		msg match {
			case FLSystemManagerTerminated() => 
				context.log.info("FL SYstem Manager has been terminated")
				this
		}
	}

	override def onSignal: PartialFunction[Signal, Behavior[Command]] = {
		case PostStop =>
			context.log.info("Simulator Supervisor stopped")
			this
	}
}