package org.nimbleedge.envisedge

import akka.actor.typed.Behavior
import akka.actor.typed.scaladsl.Behaviors
import akka.actor.typed.scaladsl.ActorContext
import akka.actor.typed.scaladsl.AbstractBehavior
import akka.actor.typed.Signal
import akka.actor.typed.PostStop
import akka.actor.typed.ActorRef
import scala.collection.mutable.{Map => MutableMap}

object LocalRouter {
    def apply(): Behavior[Command] =
        Behaviors.setup(new LocalRouter(_))
    
    trait Command

    final case class RegisterAggregator(aggId: String, actorRef: ActorRef[Aggregator.Command]) extends Command
    final case class RemoveAggregator(aggId: String) extends Command

    // TODO
    // Add messages here
}

class LocalRouter(context: ActorContext[LocalRouter.Command]) extends AbstractBehavior[LocalRouter.Command](context) {
    import LocalRouter._
    import FLSystemManager.KafkaResponse

    // TODO
    // Add state and persistent information

    context.log.info("LocalRouter started")

    private var handlers= MutableMap[String, ActorRef[Aggregator.Command]]()

    override def onMessage(msg: Command): Behavior[Command] = 
        msg match {
            // TODO
            case RegisterAggregator(aggId, actorRef) =>
                handlers(aggId) = actorRef
                this

            case resp @ KafkaResponse(receiverId, response) => 
                handlers.get(receiverId).get ! resp
                this

            case RemoveAggregator(aggId) => 
                handlers -= aggId
                this
        }
    
    override def onSignal: PartialFunction[Signal,Behavior[Command]] = {
        case PostStop =>
            context.log.info("LocalRouter stopped")
            this
    }
}