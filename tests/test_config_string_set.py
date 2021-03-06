""" Tests for the WpConfigString class. """

import unittest

from logging import basicConfig

from wpconfigr import WpConfigString

basicConfig(level='DEBUG')


class UpdateTestCase(unittest.TestCase):
    """ Tests for the update method. """

    def test_add_string(self):
        """ Asserts that a new string property is added. """

        original = """<?php
define('WP_DEBUG', false);
"""

        config = WpConfigString(content=original)
        config.set(key='WP_FOO', value='bar')

        expected = """<?php
define('WP_FOO', 'bar');
define('WP_DEBUG', false);
"""

        self.assertEqual(config.content, expected)

    def test_add_bool(self):
        """ Asserts that a new boolean property is added. """

        config = WpConfigString(content='<?php\ndefine(\'WP_DEBUG\', false);')
        config.set(key='WP_FOO', value=True)
        self.assertEqual(config.content,
                         '<?php\ndefine(\'WP_FOO\', true);\n'
                         'define(\'WP_DEBUG\', false);')

    def test_replace_bool(self):
        """ Asserts that boolean value is replaced. """

        config = WpConfigString(content='define(\'WP_DEBUG\', false);')
        config.set(key='WP_DEBUG', value=True)
        self.assertEqual(config.content, 'define(\'WP_DEBUG\', true);')

    def test_replace_empty(self):
        """ Asserts that an empty value is replaced. """

        config = 'define(\'DB_USER\', \'\');'

        updater = WpConfigString(content=config)
        updater.set(key='DB_USER', value='updated-db-user')

        expected_config = 'define(\'DB_USER\', \'updated-db-user\');'

        self.assertEqual(updater.content, expected_config)

    def test_replace_value_with_spaces(self):
        """ Asserts that value containing spaces is replaced. """

        config = 'define(\'DB_USER\', \'foo bar\');'

        updater = WpConfigString(content=config)
        updater.set(key='DB_USER', value='updated-db-user')

        expected_config = 'define(\'DB_USER\', \'updated-db-user\');'

        self.assertEqual(updater.content, expected_config)

    def test_single_replacement(self):
        """ Asserts that a single match is replaced. """
        config = """
<?php
define('DB_NAME', 'foo');
define('DB_USER', 'bar');
"""

        updater = WpConfigString(content=config)
        updater.set(key='DB_NAME', value='updated-db-name')

        expected_config = """
<?php
define('DB_NAME', 'updated-db-name');
define('DB_USER', 'bar');
"""

        self.assertEqual(updater.content, expected_config)


    def test_does_not_replace_comment(self):
        """ Asserts that a comment is not updated. """

        original = """<?php
// define('WP_DEBUG', false);
"""

        config = WpConfigString(content=original)
        config.set(key='WP_DEBUG', value=True)

        expected = """<?php
define('WP_DEBUG', true);
// define('WP_DEBUG', false);
"""

        self.assertEqual(config.content, expected)

    def test_space_variants(self):
        """ Asserts that spaces are handled. """

        def _assert(config, expect):
            updater = WpConfigString(content=config)
            updater.set(key='DB_NAME', value='new')
            self.assertEqual(updater.content, expect)

        _assert(config='define(\'DB_NAME\', \'old\');',
                expect='define(\'DB_NAME\', \'new\');')

        _assert(config=' define(\'DB_NAME\', \'old\');',
                expect=' define(\'DB_NAME\', \'new\');')

        _assert(config='define (\'DB_NAME\', \'old\');',
                expect='define (\'DB_NAME\', \'new\');')

        _assert(config='define( \'DB_NAME\', \'old\');',
                expect='define( \'DB_NAME\', \'new\');')

        _assert(config='define(\'DB_NAME\' , \'old\');',
                expect='define(\'DB_NAME\' , \'new\');')

        _assert(config='define(\'DB_NAME\',  \'old\');',
                expect='define(\'DB_NAME\',  \'new\');')

        _assert(config='define(\'DB_NAME\', \'old\' );',
                expect='define(\'DB_NAME\', \'new\' );')

        _assert(config='define(\'DB_NAME\', \'old\') ;',
                expect='define(\'DB_NAME\', \'new\') ;')

        _assert(config='define(\'DB_NAME\', \'old\'); ',
                expect='define(\'DB_NAME\', \'new\'); ')


if __name__ == '__main__':
    unittest.main()
