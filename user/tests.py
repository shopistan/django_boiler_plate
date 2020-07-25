"""
 test file to test functions
"""
import datetime


# Create your tests here.

def point_expiry_alerts():
    """

    Returns:

    """
    now = datetime.datetime.now()
    now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    print(now)


def point_transaction_history(customer_id=None):
    """

    Args:
        customer_id:

    Returns:

    """
    if customer_id:
        pass
    else:
        pass


if __name__ == '__main__':
    point_expiry_alerts()
