from DnaBucket import *


class DualBucket:
    def __init__(self, name, amount) -> None:
        self.name = name
        self.initial_amount = amount
        self.val_bucket = DnaBucket(name+"_val", amount)
        if amount == Amounts.ON:
            inv_amount = Amounts.OFF
        elif amount == Amounts.OFF:
            inv_amount = Amounts.ON
        else:
            inv_amount = amount
        self.inv_bucket = DnaBucket(name+"_inv", inv_amount)

    def print_bucket(self) -> None:
        print("\t\t" + "Dual Bucket - " + self.name + ": ")
        self.val_bucket.print_bucket()
        self.inv_bucket.print_bucket()

    def get_buckets_as_list(self) -> list:
        return [self.val_bucket, self.inv_bucket]

    def tostring(self):
        return "DualBucket(\"" + self.name + "\", " + str(self.initial_amount) + ")"
