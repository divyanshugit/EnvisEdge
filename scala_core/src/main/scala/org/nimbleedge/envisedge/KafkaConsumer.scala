package org.nimbleedge.envisedge

import Utils._

import akka.actor.typed.Behavior
import akka.actor.typed.scaladsl.Behaviors
import akka.actor.typed.scaladsl.ActorContext
import akka.actor.typed.scaladsl.AbstractBehavior
import akka.actor.typed.Signal
import akka.actor.typed.ActorRef
import akka.NotUsed
import com.typesafe.config.Config
import org.apache.kafka.clients.consumer.{KafkaConsumer => KConsumer,ConsumerRecords}
import scala.jdk.CollectionConverters._
import java.time.Duration
import FLSystemManager.KafkaResponse

object KafkaConsumer {
    def apply(config: Config, replyTo: Either[ActorRef[LocalRouter.Command], ActorRef[FLSystemManager.Command]]): Behavior[NotUsed] =
        Behaviors.setup { context =>
            val ty = replyTo match {
                case Left(_) => "Aggregator"
                case Right(_) => "FLSystemManager"
            }
            context.log.info("{} KafkaConsumer started", ty)

            val consumer = new KConsumer[String, String](config.toMap.asJava)
            consumer.subscribe(ConfigManager.getConsumerTopics(ty).asJava)

            while(true) {
                val records = consumer.poll(Duration.ofSeconds(10))
                records.forEach((record) => 
                    replyTo match {
                        case Left(l) => l ! KafkaResponse(record.key(), record.value())
                        case Right(r) => r ! KafkaResponse(record.key(), record.value())
                    }
                )
            }

            Behaviors.stopped
        }
    
}