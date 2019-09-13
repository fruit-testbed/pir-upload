#!/usr/bin/env python3

import RPi.GPIO as GPIO
import asyncio
import syndicate.mini.core as S
from syndicateutils import poller

PIR = S.Record.makeConstructor('PIR', 'host activity')
OverlayNode = S.Record.makeConstructor('OverlayNode', 'id')

DATA_PIN = 32
GPIO.setmode(GPIO.BOARD)
GPIO.setup(DATA_PIN, GPIO.IN)

loop = asyncio.get_event_loop()

local_conn = S.Connection.from_url('ws://172.17.0.1:8000/#local')
federated_conn = S.Connection.from_url('ws://172.17.0.1:8000/#test')

def discover_hostname(conn):
    with conn.turn() as t:
        a = conn.actor()
        with a.react(t) as facet:
            print('Waiting to discover node ID...')
            def on_discovery(t, node_id):
                print('Discovered node ID', repr(node_id))
                sample_and_publish(federated_conn, node_id)
                a.stop(t)
            facet.add(S.Observe(OverlayNode(S.CAPTURE)), on_add=on_discovery)

def sample_and_publish(conn, hostname):
    with conn.turn() as t:
        with conn.actor().react(t) as facet:
            def sample(facet):
                pin = GPIO.input(DATA_PIN)
                item = PIR(hostname, bool(pin))
                print(item)
                facet.add(item)
            facet.on_start(lambda turn: poller(turn, facet, 1, sample, loop))

discover_hostname(local_conn)

loop.create_task(local_conn.reconnecting_main(loop))
loop.create_task(federated_conn.reconnecting_main(loop))
loop.run_forever()
# loop.run_until_complete(federated_conn.reconnecting_main(loop))
