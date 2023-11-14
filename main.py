"""
Точка входа в стратегию
"""

from strategy_bridge.common import config
from strategy_bridge.processors import RobotCommandsSender, VisionDetectionsCollector
from strategy_bridge.processors.referee_commands_collector import (
    RefereeCommandsCollector,
)
from strategy_bridge.runner import Runner

import bridge.processors.const as const
import bridge.processors.strategy as strategy
from bridge.processors.python_controller import SSLController
from bridge.processors.robot_command_sink import CommandSink

if __name__ == "__main__":

    config.init_logging("./logs")

    # TODO: Move list of processors to config
    PROCESSORS = [
        VisionDetectionsCollector(processing_pause=0.001, should_debug=True),
        RefereeCommandsCollector(processing_pause=0.001, should_debug=True),
        SSLController(
            # should_debug=True,
            processing_pause=const.Ts,  # type:ignore
            # reduce_pause_on_process_time=True,
            dbg_game_status=strategy.GameStates.RUN,
            dbg_state=strategy.States.ATTACK,
        ),
        # SSLController(
        #     our_color='b',
        #     should_debug=True,
        #     processing_pause=const.Ts,
        #     reduce_pause_on_process_time=True,
        #     dbg_game_status = strategy.GameStates.RUN,
        #     dbg_state = strategy.States.DEFENCE),
        CommandSink(processing_pause=const.Ts / 2),  # , should_debug=True
        RobotCommandsSender(processing_pause=const.Ts / 2, should_debug=True),
    ]

    RUNNER = Runner(processors=PROCESSORS)
    RUNNER.run()
