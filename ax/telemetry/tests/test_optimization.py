#!/usr/bin/env fbpython
# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from ax.service.scheduler import Scheduler, SchedulerOptions
from ax.telemetry.optimization import OptimizationCreatedRecord
from ax.telemetry.scheduler import SchedulerCreatedRecord
from ax.utils.common.testutils import TestCase
from ax.utils.testing.core_stubs import get_branin_experiment
from ax.utils.testing.modeling_stubs import get_generation_strategy


class TestOptimization(TestCase):
    def test_flatten(self) -> None:
        scheduler = Scheduler(
            experiment=get_branin_experiment(),
            generation_strategy=get_generation_strategy(),
            options=SchedulerOptions(
                total_trials=0,
                tolerated_trial_failure_rate=0.2,
                init_seconds_between_polls=10,
            ),
        )

        record = OptimizationCreatedRecord(
            scheduler_created_record=SchedulerCreatedRecord.from_scheduler(
                scheduler=scheduler
            ),
            product_surface="Axolotl",
            launch_surface="web",
            deployed_job_id=1118,
            trial_evaluation_identifier="train",
            is_manual_generation_strategy=True,
            warm_started_from=None,
            num_custom_trials=0,
        )

        flat = record.flatten()
        expected_dict = {
            **SchedulerCreatedRecord.from_scheduler(scheduler=scheduler).flatten(),
            "product_surface": "Axolotl",
            "launch_surface": "web",
            "deployed_job_id": 1118,
            "trial_evaluation_identifier": "train",
            "is_manual_generation_strategy": True,
            "warm_started_from": None,
            "num_custom_trials": 0,
        }

        self.assertEqual(flat, expected_dict)