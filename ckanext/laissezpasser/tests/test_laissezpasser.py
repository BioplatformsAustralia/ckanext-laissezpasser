import pytest
from ckanext.laissezpasser import laissezpasser


class TestLaissezPasser:
    def test_restore(self, laissezpasser):
        # check no passes
        laissezpasser.restore()
        assert not laissezpasser

        # check no passes after restore from user obj
        laissezpasser.add("hello")
        laissezpasser.restore()
        assert not laissezpasser

        # add add a pass
        laissezpasser.add("hello")
        laissezpasser.save()

        laissezpasser.restore()
        assert laissezpasser

    def test_check(self, laissezpasser):
        # check no passes
        laissezpasser.clear()
        assert not laissezpasser

        # check no pass for hello
        assert not laissezpasser.check("hello")

        # add pass
        laissezpasser.add("hello")

        # check pass for hello
        assert not laissezpasser.check("fake")
        assert laissezpasser.check("hello")

        # clear, and then recheck
        laissezpasser.clear()
        assert not laissezpasser.check("hello")

    def test_valid(self, laissezpasser):
        # check no passes
        laissezpasser.clear()
        assert not laissezpasser

        # check no pass for hello
        assert not laissezpasser.check("hello")

        # check no valid pass for hello
        assert not laissezpasser.valid("hello")

        # add pass
        laissezpasser.add("hello")

        # check pass for hello
        assert not laissezpasser.check("fake")
        assert laissezpasser.check("hello")

        # check valid pass for hello - defaults
        assert not laissezpasser.valid("fake")
        assert laissezpasser.valid("hello")

        # clear, and then recheck
        laissezpasser.clear()
        assert not laissezpasser.check("hello")
        assert not laissezpasser.valid("hello")

        # add pass with expired date
        laissezpasser.add("hello", passdatetime="2020-07-30T03:17:41.866523")
        assert laissezpasser.check("hello")
        assert not laissezpasser.valid("hello")
