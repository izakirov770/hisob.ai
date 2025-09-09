from services.categorizer import guess_category

def test_food():
    assert guess_category("kofe latte") == "food"

def test_transport():
    assert guess_category("taksi uchun 15000") == "transport"

def test_salary():
    assert guess_category("oylik keldi 3mln") == "salary"

def test_other_default():
    assert guess_category("") == "other"
    assert guess_category("random text") == "other"
