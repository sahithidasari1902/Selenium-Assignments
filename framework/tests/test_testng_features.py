"""
Assignment 6 (TestNG) - the same features shown with pytest.
No browser needed, so these run in a second:   pytest tests/test_testng_features.py -s

TestNG                       ->  pytest
@BeforeSuite / @AfterSuite   ->  fixture(scope="session")
@BeforeClass / @AfterClass   ->  fixture(scope="class") or setup_class / teardown_class
@BeforeMethod / @AfterMethod ->  fixture (function scope) or setup_method / teardown_method
testng.xml                   ->  pytest.ini + command line options
groups                       ->  @pytest.mark.<group>   then  pytest -m smoke
priority                     ->  @pytest.mark.order(n)            (pytest-order plugin)
enabled=false                ->  @pytest.mark.skip
dependsOnMethods             ->  @pytest.mark.depends_on("name")  (defined in conftest.py)
invocationCount              ->  @pytest.mark.repeat(n)           (pytest-repeat plugin)
@Parameters                  ->  command line option / config file
@DataProvider                ->  @pytest.mark.parametrize
parallel="methods"           ->  pytest -n 4                       (pytest-xdist plugin)
Assert.assertEquals etc.     ->  plain assert
"""
import pytest

pytestmark = pytest.mark.demo
ORDER = []


# ---- 1. Order of execution of the annotations ----
@pytest.fixture(scope="session", autouse=True)
def before_suite():
    print("\n@BeforeSuite  (session fixture - start)")
    yield
    print("\n@AfterSuite   (session fixture - end)")


class TestAnnotationOrder:
    @classmethod
    def setup_class(cls):
        print("\n  @BeforeClass")

    @classmethod
    def teardown_class(cls):
        print("\n  @AfterClass")

    def setup_method(self, method):
        print(f"\n    @BeforeMethod before {method.__name__}")

    def teardown_method(self, method):
        print(f"\n    @AfterMethod after {method.__name__}")

    def test_one(self):
        print("      @Test test_one")

    def test_two(self):
        print("      @Test test_two")


# ---- 4. Assertions ----
def test_assertions():
    assert 2 + 2 == 4                          # assertEquals
    assert "Magnus" != "Login"                 # assertNotEquals
    assert "Employee" in "Employee Search"     # assertTrue(contains)
    assert not []                              # assertFalse
    assert None is None                        # assertNull
    with pytest.raises(ZeroDivisionError):     # expectedExceptions
        _ = 1 / 0


# ---- 5. Disable / ignore a test ----
@pytest.mark.skip(reason="Disabled like enabled=false in TestNG")
def test_disabled():
    assert False


# ---- 6. Dependent tests ----
def test_create_record():
    assert True


@pytest.mark.depends_on("test_create_record")
def test_edit_record():
    """Runs only if test_create_record passed (dependsOnMethods)."""
    assert True


# ---- 7. Priority ----
@pytest.mark.order(3)
def test_priority_third():
    ORDER.append(3)


@pytest.mark.order(2)
def test_priority_second():
    ORDER.append(2)


@pytest.mark.order(1)
def test_priority_first():
    ORDER.append(1)


# ---- 8. invocationCount ----
@pytest.mark.repeat(3)
def test_runs_three_times():
    assert True


# ---- 9 + 10. Parameters and DataProvider ----
@pytest.mark.parametrize("a,b,total", [(1, 2, 3), (10, 20, 30), (-5, 5, 0)])
def test_data_provider(a, b, total):
    assert a + b == total


# ---- 11. Groups ----
@pytest.mark.smoke
def test_in_smoke_group():
    assert True


@pytest.mark.regression
def test_in_regression_group():
    assert True
