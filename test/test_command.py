# coding=utf-8
import sys
import unittest
from bgmi.command import CommandParser


class CommandTest(unittest.TestCase):

    def test_argument_name(self):
        c = CommandParser()
        group_1 = c.add_arg_group('test')
        group_1.add_argument('--id-aa--', arg_type='1')
        sys.argv = ['test.py', '--id-aa--', '123456']
        namespace_1 = c.parse_command()

        self.assertEqual(namespace_1.id_aa__, '123456')

    def test_parse_positional_argument(self):
        c = CommandParser()
        group_1 = c.add_arg_group('test')
        group_1.add_argument('method')
        group_1.add_argument('sub_method')
        sys.argv = ['test.py', 'method_test', 'sub_method_test']
        namespace_1 = c.parse_command()

        self.assertEqual(namespace_1.method, 'method_test')
        self.assertEqual(namespace_1.sub_method, 'sub_method_test')

    def test_sub_parser(self):
        c = CommandParser()
        group_1 = c.add_arg_group('test')
        sub_1 = group_1.add_sub_parser('--sub_action')
        sub_2 = group_1.add_sub_parser('--sub_action2')

        # conflict action name: --sub_action
        self.assertRaises(SystemExit, group_1.add_sub_parser, '--sub_action')

        sub_1.add_argument('--force')
        sub_1.add_argument('--id', arg_type='+')
        sub_2.add_argument('--verbose', arg_type='+')

        sys.argv = ['test.py', '--sub_action', '--force']
        namespace_1 = c.parse_command()
        self.assertEqual(namespace_1.sub_action.force, True)

        sys.argv = ['test.py', '--sub_action', '--force', '--sub_action2', '--verbose', '1']
        # unrecognized arguments: --sub_action2
        self.assertRaises(SystemExit, c.parse_command)

        sys.argv = ['test.py', '--sub_action2', '--force']
        # unrecognized arguments: --force
        self.assertRaises(SystemExit, c.parse_command)
        self.assertEqual(namespace_1.sub_action.force, True)

        sys.argv = ['test.py', '--sub_action2', '--verbose', '666']
        namespace_1 = c.parse_command()
        self.assertEqual(namespace_1.sub_action2.verbose, ['666', ])

        d = CommandParser()
        group_2 = d.add_arg_group('action')
        s_1 = group_2.add_sub_parser('update')
        s_1.add_argument('subaction')
        s_2 = group_2.add_sub_parser('delete')
        s_2.add_argument('--subaction2')

        sys.argv = ['test.py', 'update', 'help']
        namespace_2 = d.parse_command()
        self.assertEqual(namespace_2.update.subaction, 'help')

        sys.argv = ['test.py', 'delete', '--subaction2']
        namespace_2 = d.parse_command()
        self.assertEqual(namespace_2.delete.subaction2, True)

    def test_parse_command(self):
        c = CommandParser()
        group_1 = c.add_arg_group('test')
        # positional argument
        group_1.add_argument('method')
        group_1.add_argument('-v', dest='verbose', default=False)
        group_1.add_argument('--id', dest='id', arg_type='1', default=False)
        group_1.add_argument('--id2', dest='id2', arg_type='+')
        group_1.add_argument('--id3', dest='id3', arg_type='+')

        sys.argv = ['test.py', 'method_test1']
        namespace_1 = c.parse_command()
        self.assertFalse(namespace_1.verbose)

        sys.argv = ['test.py', 'method_test2', '-v']
        namespace_2 = c.parse_command()
        self.assertTrue(namespace_2.verbose)

        sys.argv = ['test.py', 'method_test3', '-v', '--id', '1', '--id2', '1', '2']
        namespace_3 = c.parse_command()
        self.assertEqual(namespace_3.method, 'method_test3')
        self.assertEqual(namespace_3.id, '1')
        self.assertEqual(namespace_3.id2, ['1', '2'])

    def test_choice(self):
        c = CommandParser()
        g1 = c.add_arg_group('test')
        g1.add_argument('--method', arg_type='1', choice=('GET', 'POST', 'HEAD', ))
        sys.argv = ['test.py', '--method', 'PUT']
        self.assertRaises(SystemExit, c.parse_command)

        c = CommandParser()
        g2 = c.add_arg_group('test')
        sub_1 = g2.add_sub_parser('--get-method')
        sub_1.add_argument('--get', arg_type='1', choice=('GET', 'HEAD', ), default='GET')

        sub_2 = g2.add_sub_parser('--post-method')
        sub_2.add_argument('--post', arg_type='1', choice=('POST', 'PUT', ))

        sub_3 = g2.add_sub_parser('get-method')
        sub_3.add_argument('--verbose')

        sys.argv = ['test.py', '--get-method']
        namespace = c.parse_command()
        print namespace


if __name__ == '__main__':
    unittest.main()