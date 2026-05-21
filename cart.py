import math
from enum import Enum


class MembershipRank(str, Enum):
    GENERAL = "general"
    PREMIUM = "premium"


class Coupon(str, Enum):
    NONE = "none"
    PERCENT_10_OFF = "10%_off"
    YEN_500_OFF = "500_off"


def _apply_membership_discount(amount: int, rank: MembershipRank) -> int:
    if rank == MembershipRank.PREMIUM:
        return math.floor(amount * 0.95)
    return amount


def _apply_coupon(amount: int, coupon: Coupon) -> int:
    if coupon == Coupon.PERCENT_10_OFF:
        return math.floor(amount * 0.9)
    if coupon == Coupon.YEN_500_OFF:
        return max(0, amount - 500)
    return amount


def _apply_points(amount: int, points_to_use: int) -> tuple[int, int]:
    consumed = min(points_to_use, amount)
    return amount - consumed, consumed


def calculate_cart(
    total_amount: int,
    membership_rank: str,
    coupon: str,
    points_to_use: int,
) -> tuple[int, int]:
    rank = MembershipRank(membership_rank)
    coupon_type = Coupon(coupon)

    amount = _apply_membership_discount(total_amount, rank)
    amount = _apply_coupon(amount, coupon_type)
    payment, consumed_points = _apply_points(amount, points_to_use)

    return payment, consumed_points
