import asyncio

def poller(initial_turn, outer_facet, interval_sec, callback, loop=None):
    if loop is None:
        loop = asyncio.get_event_loop()

    def teardown_and_setup(current_deadline, previous_facet):
        with outer_facet.conn.turn() as turn:
            setup(turn, current_deadline)
            previous_facet.stop(turn)

    def setup(turn, current_deadline):
        if outer_facet.is_alive():
            with outer_facet.react(turn) as facet:
                if callback(facet) is not False:
                    next_deadline = current_deadline + interval_sec
                    loop.call_at(next_deadline, teardown_and_setup, next_deadline, facet)

    if not outer_facet.is_alive():
        raise Exception('Cannot start poller in dead facet; did you forget an on_start?')
    setup(initial_turn, loop.time())
