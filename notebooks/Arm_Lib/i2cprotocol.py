#! /usr/bin/env python3

class I2CPrinter(object):
    def __init__(self):
       self.hpattern = ['┌', '─', '┐', '│']
       self.lpattern = ['─', '┘', '└', '┴']

    def print_i2c_block_data(self, address, register, data, inc_scl=True, inc_sda=True, inc_bits=True,
                             inc_add_data=True):
        i2c_bits_msg = f"s {address:08b} w a {register:08b} a {data[0]:08b} a {data[1]:08b} a {data[2]:08b} a {data[3]:08b} a p"
        i2c_adr_data_msg = f"s 0x{address:02x} w a 0x{register:02x} a 0x{data[0]:02x} a 0x{data[1]:02x} a 0x{data[2]:02x} a 0x{data[3]:02x} a p"

        print(i2c_bits_msg.replace(' ', '') + "\n")

        if inc_scl:
            offset_l1 = " " * 5
            offset_h1 = " " * 2
            len_signal = len(i2c_bits_msg.replace(' ', '')) - 2
            scl_h = f"{self.hpattern[1] * 5}{self.hpattern[2]}{offset_h1}" + f"{self.hpattern[0]}{self.hpattern[1]}{self.hpattern[2]} " * len_signal + \
                    f"{self.hpattern[0]}{self.hpattern[1] * 3}"
            scl_l = f"{offset_l1}{self.lpattern[2]}{self.lpattern[0] * 2}" + f"{self.lpattern[1]} {self.lpattern[2]}{self.lpattern[0]}" * len_signal + \
                    self.lpattern[1]
            print(f"scl: {scl_h}\n     {scl_l}")

        if inc_sda:
            scl_l = ''
            scl_h = ''
            old_cr = ''
            to_up = False
            to_down = False
            for cr in i2c_bits_msg.replace(' ', ''):
                if old_cr == '':
                    old_cr = cr
                if cr == 'w':
                    cr = '0'
                elif cr == 'r':
                    cr = '1'
                if old_cr != cr:
                    if old_cr == '1':
                        to_down = True
                    elif old_cr == '0':
                        to_up = True
                    old_cr = cr
                if cr == 's':
                    scl_h += f"{self.hpattern[1] * 3}{self.hpattern[2]} "
                    scl_l += f"   {self.lpattern[2]}{self.lpattern[0]}"
                if cr == 'p':
                    pass
                if cr == '0':
                    scl_l += self.lpattern[2] if to_down else self.lpattern[0]
                    scl_l += self.lpattern[0]
                    scl_l += self.lpattern[1] if to_up else self.lpattern[0]
                    scl_h += self.hpattern[2] if to_down else ' '
                    scl_h += ' ' * 2
                    if to_up:
                        to_up = False
                    if to_down:
                        to_down = False
                if cr == '1':
                    scl_l += self.lpattern[1] if to_up else ' '
                    scl_l += ' ' * 2
                    scl_h += self.hpattern[0] if to_up else self.hpattern[1]
                    scl_h += self.hpattern[1]
                    scl_h += self.hpattern[2] if to_down else self.hpattern[1]
                    if to_up:
                        to_up = False
                    if to_down:
                        to_down = False
                if cr == 'a':
                    scl_l += self.lpattern[3]
                    scl_h += self.hpattern[3]
                    to_up = to_down = False

            print(f"sda: {scl_h}\n     {scl_l}")

        if inc_bits:
            print(f"\ni2c bits: {i2c_bits_msg}")

        if inc_add_data:
            print(f"\ni2c address: {i2c_adr_data_msg}\n       data")

