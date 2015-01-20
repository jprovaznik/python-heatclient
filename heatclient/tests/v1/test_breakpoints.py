# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mock
import testtools

import heatclient.v1.shell as shell


class TestBreakpoints(testtools.TestCase):
    def setUp(self):
        super(TestBreakpoints, self).setUp()
        self.client = mock.Mock()
        nested_stack = mock.Mock()
        self.client.resources.get = mock.Mock(name='thingy',
                                              return_value=nested_stack)
        type(nested_stack).physical_resource_id = mock.PropertyMock(
            return_value='nested_id')
        self.args = mock.Mock()
        stack_name_p = mock.PropertyMock(return_value="mystack")
        type(self.args).name = stack_name_p
        type(self.args).id = stack_name_p
        shell.template_utils.get_template_contents = mock.Mock(
            return_value=({}, ""))
        shell.template_utils.process_multiple_environments_and_files = \
            mock.Mock(return_value=({}, {}))
        shell.utils.format_parameters = mock.Mock(return_value=[])
        shell.do_stack_list = mock.Mock()
        shell.logger = mock.Mock()
        type(self.args).clear_parameter = mock.PropertyMock(return_value=[])
        type(self.args).rollback = mock.PropertyMock(return_value=None)

    def test_create_breakpoints_in_args(self):
        type(self.args).breakpoint = mock.PropertyMock(
            return_value=['bp', 'another_bp'])

        shell.do_stack_create(self.client, self.args)
        self.client.stacks.create.assert_called_once()
        actual_breakpoints = self.client.stacks.create.call_args[1][
            'environment']['breakpoints']
        self.assertEqual([['mystack', 'bp'], ['mystack', 'another_bp']],
                         actual_breakpoints)

    def test_create_nested_breakpoints_in_args(self):
        type(self.args).breakpoint = mock.PropertyMock(
            return_value=['nested/bp', 'super/nested/bp'])

        shell.do_stack_create(self.client, self.args)
        self.client.stacks.create.assert_called_once()
        actual_breakpoints = self.client.stacks.create.call_args[1][
            'environment']['breakpoints']
        self.assertEqual([['mystack', 'nested', 'bp'],
                          ['mystack', 'super', 'nested', 'bp']],
                         actual_breakpoints)

    def test_create_breakpoints_in_env(self):
        type(self.args).breakpoint = mock.PropertyMock(return_value=None)

        env = {'breakpoints': ['bp', 'another_bp']}
        shell.template_utils.process_multiple_environments_and_files = \
            mock.Mock(return_value=({}, env))

        shell.do_stack_create(self.client, self.args)
        self.client.stacks.create.assert_called_once()
        actual_breakpoints = self.client.stacks.create.call_args[1][
            'environment']['breakpoints']
        self.assertEqual([['mystack', 'bp'], ['mystack', 'another_bp']],
                         actual_breakpoints)

    def test_create_nested_breakpoints_in_env(self):
        type(self.args).breakpoint = mock.PropertyMock(return_value=None)
        env = {
            'breakpoints': [
                ['nested', 'bp'],
                ['super', 'nested', 'another_bp'],
            ]
        }
        shell.template_utils.process_multiple_environments_and_files = \
            mock.Mock(return_value=({}, env))

        shell.do_stack_create(self.client, self.args)
        self.client.stacks.create.assert_called_once()
        actual_breakpoints = self.client.stacks.create.call_args[1][
            'environment']['breakpoints']
        expected_breapoints = [
            ['mystack', 'nested', 'bp'],
            ['mystack', 'super', 'nested', 'another_bp'],
        ]
        self.assertEqual(expected_breapoints, actual_breakpoints)

    def test_create_breakpoints_in_env_and_args(self):
        type(self.args).breakpoint = mock.PropertyMock(return_value=[
            'nested_a/bp',
            'bp_a',
            'another_bp_a',
            'super_a/nested/bp',
        ])
        env = {
            'breakpoints': [
                ['nested_e', 'bp'],
                'bp_e',
                'another_bp_e',
                ['super_e', 'nested', 'bp'],
            ]
        }
        shell.template_utils.process_multiple_environments_and_files = \
            mock.Mock(return_value=({}, env))

        shell.do_stack_create(self.client, self.args)
        self.client.stacks.create.assert_called_once()
        actual_breakpoints = self.client.stacks.create.call_args[1][
            'environment']['breakpoints']
        expected_breapoints = [
            ['mystack', 'bp_a'],
            ['mystack', 'another_bp_a'],
            ['mystack', 'nested_a', 'bp'],
            ['mystack', 'super_a', 'nested', 'bp'],
            ['mystack', 'bp_e'],
            ['mystack', 'another_bp_e'],
            ['mystack', 'nested_e', 'bp'],
            ['mystack', 'super_e', 'nested', 'bp'],
        ]
        self.assertEqual(sorted(expected_breapoints),
                         sorted(actual_breakpoints))

    def test_update_breakpoints_in_args(self):
        type(self.args).breakpoint = mock.PropertyMock(
            return_value=['bp', 'another_bp'])

        shell.do_stack_update(self.client, self.args)
        self.client.stacks.update.assert_called_once()
        actual_breakpoints = self.client.stacks.update.call_args[1][
            'environment']['breakpoints']
        self.assertEqual([['mystack', 'bp'], ['mystack', 'another_bp']],
                         actual_breakpoints)

    def test_update_nested_breakpoints_in_args(self):
        type(self.args).breakpoint = mock.PropertyMock(
            return_value=['nested/bp', 'super/nested/bp'])

        shell.do_stack_update(self.client, self.args)
        self.client.stacks.update.assert_called_once()
        actual_breakpoints = self.client.stacks.update.call_args[1][
            'environment']['breakpoints']
        self.assertEqual([['mystack', 'nested', 'bp'],
                          ['mystack', 'super', 'nested', 'bp']],
                         actual_breakpoints)

    def test_update_breakpoints_in_env(self):
        type(self.args).breakpoint = mock.PropertyMock(return_value=None)

        env = {'breakpoints': ['bp', 'another_bp']}
        shell.template_utils.process_multiple_environments_and_files = \
            mock.Mock(return_value=({}, env))

        shell.do_stack_update(self.client, self.args)
        self.client.stacks.update.assert_called_once()
        actual_breakpoints = self.client.stacks.update.call_args[1][
            'environment']['breakpoints']
        self.assertEqual([['mystack', 'bp'], ['mystack', 'another_bp']],
                         actual_breakpoints)

    def test_update_nested_breakpoints_in_env(self):
        type(self.args).breakpoint = mock.PropertyMock(return_value=None)

        env = {
            'breakpoints': [
                ['nested', 'bp'],
                ['super', 'nested', 'another_bp'],
            ]
        }
        shell.template_utils.process_multiple_environments_and_files = \
            mock.Mock(return_value=({}, env))

        shell.do_stack_update(self.client, self.args)
        self.client.stacks.update.assert_called_once()
        actual_breakpoints = self.client.stacks.update.call_args[1][
            'environment']['breakpoints']
        expected_breapoints = [
            ['mystack', 'nested', 'bp'],
            ['mystack', 'super', 'nested', 'another_bp'],
        ]
        self.assertEqual(expected_breapoints, actual_breakpoints)

    def test_update_breakpoints_in_env_and_args(self):
        type(self.args).breakpoint = mock.PropertyMock(return_value=[
            'nested_a/bp',
            'bp_a',
            'another_bp_a',
            'super_a/nested/bp',
        ])
        env = {
            'breakpoints': [
                ['nested_e', 'bp'],
                'bp_e',
                'another_bp_e',
                ['super_e', 'nested', 'bp'],
            ]
        }
        shell.template_utils.process_multiple_environments_and_files = \
            mock.Mock(return_value=({}, env))

        shell.do_stack_update(self.client, self.args)
        self.client.stacks.update.assert_called_once()
        actual_breakpoints = self.client.stacks.update.call_args[1][
            'environment']['breakpoints']
        expected_breapoints = [
            ['mystack', 'bp_a'],
            ['mystack', 'another_bp_a'],
            ['mystack', 'nested_a', 'bp'],
            ['mystack', 'super_a', 'nested', 'bp'],
            ['mystack', 'bp_e'],
            ['mystack', 'another_bp_e'],
            ['mystack', 'nested_e', 'bp'],
            ['mystack', 'super_e', 'nested', 'bp'],
        ]
        self.assertEqual(sorted(expected_breapoints),
                         sorted(actual_breakpoints))

    def test_clear_breakpoint(self):
        type(self.args).breakpoint = mock.PropertyMock(
            return_value=['bp'])

        shell.do_breakpoint_clear(self.client, self.args)
        payload = self.client.resources.signal.call_args[1]
        self.assertEqual(payload['data'], {'breakpoint': False})
        self.assertEqual(payload['resource_name'], 'bp')
        self.assertEqual(payload['stack_id'], 'mystack')

    def test_clear_nested_breakpoint(self):
        type(self.args).breakpoint = mock.PropertyMock(
            return_value=['a/b/bp'])

        shell.do_breakpoint_clear(self.client, self.args)
        payload = self.client.resources.signal.call_args[1]
        self.assertEqual(payload['data'], {'breakpoint': False})
        self.assertEqual(payload['resource_name'], 'bp')
        self.assertEqual(payload['stack_id'], 'nested_id')
