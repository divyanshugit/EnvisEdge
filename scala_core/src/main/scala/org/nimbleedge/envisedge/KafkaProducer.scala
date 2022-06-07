package org.nimbleedge.envisedge

import Utils._

import org.apache.kafka.clients.producer.{KafkaProducer => KProducer, ProducerRecord}
import scala.jdk.CollectionConverters._
import com.typesafe.config.Config

object KafkaProducer {
    def init(config: Config) = {
        producer = new KProducer[String,String](config.toMap.asJava)
    }

    def send(topic: String, key: String, value: String) = {
        producer.send(new ProducerRecord(topic, key, value))
    }

    def send_and_block(topic: String, key: String, value: String) = {
        producer.send(new ProducerRecord(topic, key, value)).get()
    }

    var producer: KProducer[String, String] = _
}

