import pytest
from cart import calculate_cart


# ---------------------------------------------------------------------------
# 通常ケース
# ---------------------------------------------------------------------------

def test_normal_no_discount_no_points():
    """一般会員・クーポンなし・ポイントなし → 割引なしでそのまま"""
    payment, consumed = calculate_cart(1000, "general", "none", 0)
    assert payment == 1000
    assert consumed == 0


def test_premium_discount_only():
    """プレミアム会員の5%割引のみ適用"""
    payment, consumed = calculate_cart(1000, "premium", "none", 0)
    assert payment == 950
    assert consumed == 0


def test_coupon_10percent_off():
    """10%オフクーポン適用（一般会員）"""
    payment, consumed = calculate_cart(2000, "general", "10%_off", 0)
    assert payment == 1800
    assert consumed == 0


def test_coupon_500_off():
    """500円引きクーポン適用（一般会員）"""
    payment, consumed = calculate_cart(2000, "general", "500_off", 0)
    assert payment == 1500
    assert consumed == 0


def test_points_applied():
    """ポイント利用（一般会員・クーポンなし）"""
    payment, consumed = calculate_cart(1000, "general", "none", 300)
    assert payment == 700
    assert consumed == 300


def test_combined_premium_coupon_points():
    """プレミアム会員 + 10%オフ + ポイント利用の複合ケース"""
    # 1000 → premium5%off → 950 → 10%off → floor(855.0) = 855 → points200 → 655
    payment, consumed = calculate_cart(1000, "premium", "10%_off", 200)
    assert payment == 655
    assert consumed == 200


# ---------------------------------------------------------------------------
# 境界値・エッジケース
# ---------------------------------------------------------------------------

def test_coupon_500_off_less_than_discount():
    """合計金額がクーポン割引額（500円）より小さい場合 → 支払金額は0円"""
    payment, consumed = calculate_cart(300, "general", "500_off", 0)
    assert payment == 0
    assert consumed == 0


def test_points_exceed_payment_clamps_to_zero():
    """ポイントが残額を超えるケース → 支払金額は0円で止まり、消費ポイントは残額分のみ"""
    # 1000 → premium5%off → 950 → クーポンなし → 950 → points2000(>950) → payment=0, consumed=950
    payment, consumed = calculate_cart(1000, "premium", "none", 2000)
    assert payment == 0
    assert consumed == 950


def test_points_exact_match():
    """ポイントが残額にちょうど一致するケース"""
    payment, consumed = calculate_cart(1000, "general", "none", 1000)
    assert payment == 0
    assert consumed == 1000


def test_10percent_off_truncates_fraction():
    """10%オフで端数が発生する場合 → 切り捨て"""
    # 1055 * 0.9 = 949.5 → floor → 949
    payment, consumed = calculate_cart(1055, "general", "10%_off", 0)
    assert payment == 949
    assert consumed == 0


def test_premium_discount_truncates_fraction():
    """プレミアム割引で端数が発生する場合 → 切り捨て"""
    # 1001 * 0.95 = 950.95 → floor → 950
    payment, consumed = calculate_cart(1001, "premium", "none", 0)
    assert payment == 950
    assert consumed == 0


def test_combined_fractions_then_points():
    """端数切り捨て後にポイント適用 → 切り捨て済み金額に対してポイントを使う"""
    # 1055 → premium5%off → floor(1002.25) = 1002 → 10%off → floor(901.8) = 901 → points100 → 801
    payment, consumed = calculate_cart(1055, "premium", "10%_off", 100)
    assert payment == 801
    assert consumed == 100


def test_zero_total_amount():
    """合計金額0円のケース → 支払金額は0円"""
    payment, consumed = calculate_cart(0, "general", "none", 0)
    assert payment == 0
    assert consumed == 0


def test_points_zero_when_payment_already_zero():
    """クーポンで支払いが0円になった後にポイントを指定しても消費は0"""
    payment, consumed = calculate_cart(300, "general", "500_off", 100)
    assert payment == 0
    assert consumed == 0
