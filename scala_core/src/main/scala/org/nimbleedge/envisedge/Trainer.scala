package org.nimbleedge.envisedge

import models._

import akka.actor.typed.Behavior
import akka.actor.typed.scaladsl.Behaviors
import akka.actor.typed.scaladsl.ActorContext
import akka.actor.typed.scaladsl.AbstractBehavior
import akka.actor.typed.Signal
import akka.actor.typed.PostStop

object Trainer {
    def apply(traId: TrainerIdentifier): Behavior[Command] =
        Behaviors.setup(new Trainer(_, traId))
    
    trait Command

    // TODO
    // Add messages here
}

class Trainer(context: ActorContext[Trainer.Command], traId: TrainerIdentifier) extends AbstractBehavior[Trainer.Command](context) {
    import Trainer._

    // TODO
    // Add state and persistent information

    context.log.info("Trainer {} started", traId.toString())

    override def onMessage(msg: Command): Behavior[Command] = {this}
        /*
        msg match {
            // TODO
            case JobResponse(message) => 
                if (message == "Timeout") {
                    context.log.info("Trainer Helper {} timeout.", traId.name())
                } else {
                    // here json object is converted to respective case class object
                    // to be used for further processing in scala
                    val response = JsonDecoder.deserialize(message)

                    // TODO
                    // Further processing with reponse
                }
                this

            case HelperTerminated(_) => 
                context.log.info("Trainer {} Helper has been terminated", traId.name())
                this
        }
        */
    
    override def onSignal: PartialFunction[Signal,Behavior[Command]] = {
        case PostStop =>
            context.log.info("Trainer {} stopped", traId.toString())
            this
    }
}
