from escpos import printer


class Printer():
    def __init__(self, vendor_id, product_id) -> None:
        self.vendor_id = int(f"0x{vendor_id}", 16)
        self.product_id = int(f"0x{product_id}", 16)

    def print_ticket(self, transaction_id, vehicle_code, created_time):
        p = printer.Usb(self.vendor_id, self.product_id)
        p.set(align='center', flip=True)
        p.qr(transaction_id, size=6, native=True)
        p.text(f"{created_time} | {vehicle_code}")
        p.cut()
        p.close()