# -------------------------------------------------------------------------
# C (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import logging
import pytest
import inspect
import threading
import concurrent.futures
from tests.common.pipeline.helpers import (
    all_except,
    make_mock_stage,
    make_mock_op_or_event,
    assert_callback_failed,
    get_arg_count,
    add_mock_method_waiter,
)
from azure.iot.device.common.pipeline.pipeline_stages_base import PipelineStage
from tests.common.pipeline.pipeline_data_object_test import add_instantiation_test
from azure.iot.device.common.pipeline import pipeline_thread

logging.basicConfig(level=logging.DEBUG)


def add_base_pipeline_stage_tests(
    test_cls,
    cls,
    all_ops,
    handled_ops,
    all_events,
    handled_events,
    methods_that_enter_pipeline_thread=[],
    methods_that_can_run_in_any_thread=[],
    extra_initializer_defaults={},
):
    """
    Add all of the "basic" tests for validating a pipeline stage.  This includes tests for
    instantiation and tests for properly handling "unhandled" operations and events".
    """

    add_instantiation_test(
        test_cls=test_cls,
        cls=cls,
        defaults={"name": cls.__name__, "next": None, "previous": None, "pipeline_root": None},
        extra_defaults=extra_initializer_defaults,
    )
    add_unknown_ops_tests(test_cls=test_cls, cls=cls, all_ops=all_ops, handled_ops=handled_ops)
    add_unknown_events_tests(
        test_cls=test_cls, cls=cls, all_events=all_events, handled_events=handled_events
    )
    add_pipeline_thread_tests(
        test_cls=test_cls,
        cls=cls,
        methods_that_enter_pipeline_thread=methods_that_enter_pipeline_thread,
        methods_that_can_run_in_any_thread=methods_that_can_run_in_any_thread,
    )


def add_unknown_ops_tests(test_cls, cls, all_ops, handled_ops):
    """
    Add tests for properly handling of "unknown operations," which are operations that aren't
    handled by a particular stage.  These operations should be passed down by any stage into
    the stages that follow.
    """
    unknown_ops = all_except(all_items=all_ops, items_to_exclude=handled_ops)

    @pytest.fixture
    def specific_op(self, op_cls, mocker):
        op = make_mock_op_or_event(op_cls)
        op.callback = mocker.MagicMock()
        add_mock_method_waiter(op, "callback")
        return op

    test_cls.specific_op = specific_op

    # BKTODO: this will need to be moved
    @pytest.fixture
    def stage(self, mocker, arbitrary_exception, arbitrary_base_exception):
        return make_mock_stage(
            mocker=mocker,
            stage_to_make=cls,
            exc_to_raise=arbitrary_exception,
            base_exc_to_raise=arbitrary_base_exception,
        )

    test_cls.stage = stage

    @pytest.mark.it("Passes unknown operation to next stage")
    @pytest.mark.parametrize("op_cls", unknown_ops)
    def test_passes_op_to_next_stage(self, op_cls, specific_op, stage):
        stage.run_op(specific_op)
        assert stage.next.run_op.call_count == 1
        assert stage.next.run_op.call_args[0][0] == specific_op

    test_cls.test_passes_op_to_next_stage = test_passes_op_to_next_stage

    @pytest.mark.it("Fails unknown operation if there is no next stage")
    @pytest.mark.parametrize("op_cls", unknown_ops)
    def test_passes_op_with_no_next_stage(self, op_cls, specific_op, stage):
        stage.next = None
        stage.run_op(specific_op)
        specific_op.wait_for_callback_to_be_called()
        assert_callback_failed(op=specific_op)

    test_cls.test_passes_op_with_no_next_stage = test_passes_op_with_no_next_stage

    @pytest.mark.it("Catches Exceptions raised when passing unknown operation to next stage")
    @pytest.mark.parametrize("op_cls", unknown_ops)
    def test_passes_op_to_next_stage_which_throws_exception(self, op_cls, specific_op, stage):
        specific_op.action = "exception"
        stage.run_op(specific_op)
        specific_op.wait_for_callback_to_be_called()
        assert_callback_failed(op=specific_op)

    test_cls.test_passes_op_to_next_stage_which_throws_exception = (
        test_passes_op_to_next_stage_which_throws_exception
    )

    @pytest.mark.it(
        "Allows BaseExceptions raised when passing unknown operation to next start to propogate"
    )
    @pytest.mark.parametrize("op_cls", unknown_ops)
    def test_passes_op_to_next_stage_which_throws_base_exception(
        self, op_cls, specific_op, stage, arbitrary_base_exception
    ):
        specific_op.action = "base_exception"
        with pytest.raises(arbitrary_base_exception.__class__) as e_info:
            stage.run_op(specific_op)
        assert e_info.value is arbitrary_base_exception

    test_cls.test_passes_op_to_next_stage_which_throws_base_exception = (
        test_passes_op_to_next_stage_which_throws_base_exception
    )


def add_unknown_events_tests(test_cls, cls, all_events, handled_events):
    """
    Add tests for properly handling of "unknown events," which are events that aren't
    handled by a particular stage.  These operations should be passed up by any stage into
    the stages that proceed it..
    """

    unknown_events = all_except(all_items=all_events, items_to_exclude=handled_events)

    if not unknown_events:
        return

    @pytest.fixture
    def specific_event(self, event_cls):
        return make_mock_op_or_event(event_cls)

    test_cls.specific_event = specific_event

    # BKTODO: this will need to be moved
    @pytest.fixture
    def previous(self, stage, mocker):
        class PreviousStage(PipelineStage):
            def __init__(self):
                super(PreviousStage, self).__init__()
                self.handle_pipeline_event = mocker.MagicMock()

            def _execute_op(self, op):
                pass

        previous = PreviousStage()
        stage.previous = previous
        return previous

    test_cls.previous = previous

    @pytest.mark.it("Passes unknown event to previous stage")
    @pytest.mark.parametrize("event_cls", unknown_events)
    def test_passes_event_to_previous_stage(self, event_cls, stage, specific_event, previous):
        stage.handle_pipeline_event(specific_event)
        assert previous.handle_pipeline_event.call_count == 1
        assert previous.handle_pipeline_event.call_args[0][0] == specific_event

    test_cls.test_passes_event_to_previous_stage = test_passes_event_to_previous_stage

    @pytest.mark.it("Calls unhandled exception handler if there is no previous stage")
    @pytest.mark.parametrize("event_cls", unknown_events)
    def test_passes_event_with_no_previous_stage(
        self, event_cls, stage, specific_event, unhandled_error_handler
    ):
        stage.handle_pipeline_event(specific_event)
        assert unhandled_error_handler.call_count == 1

    test_cls.test_passes_event_with_no_previous_stage = test_passes_event_with_no_previous_stage

    @pytest.mark.it("Catches Exceptions raised when passing unknown event to previous stage")
    @pytest.mark.parametrize("event_cls", unknown_events)
    def test_passes_event_to_previous_stage_which_throws_exception(
        self,
        event_cls,
        stage,
        specific_event,
        previous,
        unhandled_error_handler,
        arbitrary_exception,
    ):
        previous.handle_pipeline_event.side_effect = arbitrary_exception
        stage.handle_pipeline_event(specific_event)
        assert unhandled_error_handler.call_count == 1
        assert unhandled_error_handler.call_args[0][0] == arbitrary_exception

    test_cls.test_passes_event_to_previous_stage_which_throws_exception = (
        test_passes_event_to_previous_stage_which_throws_exception
    )

    @pytest.mark.it(
        "Allows BaseExceptions raised when passing unknown operation to next start to propogate"
    )
    @pytest.mark.parametrize("event_cls", unknown_events)
    def test_passes_event_to_previous_stage_which_throws_base_exception(
        self,
        event_cls,
        stage,
        specific_event,
        previous,
        unhandled_error_handler,
        arbitrary_base_exception,
    ):
        previous.handle_pipeline_event.side_effect = arbitrary_base_exception
        with pytest.raises(arbitrary_base_exception.__class__) as e_info:
            stage.handle_pipeline_event(specific_event)
        assert unhandled_error_handler.call_count == 0
        assert e_info.value is arbitrary_base_exception

    test_cls.test_passes_event_to_previous_stage_which_throws_base_exception = (
        test_passes_event_to_previous_stage_which_throws_base_exception
    )


class ThreadLaunchedError(Exception):
    pass


def add_pipeline_thread_tests(
    test_cls, cls, methods_that_enter_pipeline_thread, methods_that_can_run_in_any_thread
):
    def does_method_assert_pipeline_thread(method_name):
        if method_name.startswith("__"):
            return False
        elif method_name in methods_that_enter_pipeline_thread:
            return False
        elif method_name in methods_that_can_run_in_any_thread:
            return False
        else:
            return True

    methods_that_assert_pipeline_thread = [
        x[0]
        for x in inspect.getmembers(cls, inspect.isfunction)
        if does_method_assert_pipeline_thread(x[0])
    ]

    @pytest.fixture
    def unmocked_stage(self):
        return cls()

    test_cls.unmocked_stage = unmocked_stage

    @pytest.mark.parametrize("method_name", methods_that_assert_pipeline_thread)
    @pytest.mark.it("Enforces use of the pipeline thread when calling method")
    def test_asserts_in_pipeline(self, unmocked_stage, method_name, fake_non_pipeline_thread):
        func = getattr(unmocked_stage, method_name)
        args = [None for i in (range(get_arg_count(func) - 1))]
        with pytest.raises(AssertionError):
            func(*args)

    test_cls.test_asserts_in_pipeline = test_asserts_in_pipeline

    if methods_that_enter_pipeline_thread:

        @pytest.mark.parametrize("method_name", methods_that_enter_pipeline_thread)
        @pytest.mark.it("Automatically enters the pipeline thread when calling method")
        def test_enters_pipeline(
            self, mocker, unmocked_stage, method_name, fake_non_pipeline_thread
        ):
            func = getattr(unmocked_stage, method_name)
            args = [None for i in (range(get_arg_count(func) - 1))]

            #
            # We take a bit of a roundabout way to verify that the functuion enters the
            # pipeline executor:
            #
            # 1. we verify that the method got the pipeline executor
            # 2. we verify that the method invoked _something_ on the pipeline executor
            #
            # It's not perfect, but it's good enough.
            #
            # We do this because:
            # 1. We don't have the exact right args to run the method and we don't want
            #    to add the complexity to get the right args in this test.
            # 2. We can't replace the wrapped method with a mock, AFAIK.
            #
            pipeline_executor = pipeline_thread._get_named_executor("pipeline")
            mocker.patch.object(pipeline_executor, "submit")
            pipeline_executor.submit.side_effect = ThreadLaunchedError
            mocker.spy(pipeline_thread, "_get_named_executor")

            # If the method calls submit on some executor, it will raise a ThreadLaunchedError
            with pytest.raises(ThreadLaunchedError):
                func(*args)

            # now verify that the code got the pipeline executor and verify that it used that
            # executor to launch something.
            assert pipeline_thread._get_named_executor.call_count == 1
            assert pipeline_thread._get_named_executor.call_args[0][0] == "pipeline"
            assert pipeline_executor.submit.call_count == 1

        test_cls.test_enters_pipeline = test_enters_pipeline
