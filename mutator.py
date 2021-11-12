'''
    mutator.py
    1) use_wabt() ; wabt를 이용해서 wat을 wasm으로 mutate. 이때 wabt은 mutate를 위해 수정한 wabt
    2) make_template() ; mutate된 wasm을 bytes buffer로 만들고 dharma template에 WebAssembly.Module(buffer) 추가
    3) use_dharma() ; dharma를 이용하여 js 생성
''' 
import shutil
import subprocess
import os

# SEED = "./dir/seed/table.wat"
MUTATE_WASM_PATH = "./dir/tmp/"
SEEDDIR = "./dir/seed/"

DHARMA_TEMPLATE = "./dir/template/wasm.dg"
DHARMA_TEMPLATE_UP = "./dir/template/wasm_up.dg"
DHARMA_TEMPLATE_DOWN = "./dir/template/wasm_down.dg"

FILELIST = []

class Mutator():
    def __init__(self, args):
        self.args = args

        for i in range(args.m):
            FILELIST.append("mutate"+str(i).zfill(2)+".wasm")


    def use_wabt(self, itr):
        '''
            wabt를 이용해서 wat을 wasm으로 mutate
            **input : 1개의 ./seed/seed.wasm
            **output : 100개의 ./dir/tmp/mutate.wasm
            ./wabt/build/wat2wasm ./seed/seed.wasm
        '''
        try:
            cmd = []
            cmd.append("./wabt/build/wat2wasm")
            cmd.append(SEEDDIR + str(itr) + '.wat') 
            cmd.append("-m " + str(self.args.m))
            cmd.append("--debug-names")
            cmd = " ".join(cmd)
            subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True, shell=True, preexec_fn=os.setsid).wait()
            # print("[+] use_wabt")

        except Exception as e:
            print("[!] ERROR in use_wabt")
            print(e)


    def make_template(self):
        try:
            with open("./dir/template/dharma_template.dg", "w") as outfile:
                with open("./dir/template/wasm1.dg", "rt") as wasm1:
                    outfile.write(wasm1.read())
                for i in range(self.args.m):
                    wasm = 'mutate' + str(i).zfill(2) + '.wasm'
                    with open("./dir/mutate/" + wasm, "rb") as f:
                        data = f.read()
                        modulewasm = "  new Uint8Array(["
                        for b in data:
                            modulewasm += str(b)
                            modulewasm += ","
                        modulewasm = modulewasm[:-1]
                        modulewasm += "])\n"
                        outfile.write(str(modulewasm)) # 뮤테이트된 wasm byte array 추가
                with open("./dir/template/wasm2.dg", "rt") as wasm2:
                    outfile.write(wasm2.read())
                with open("./dir/seed/exports.txt", "rt") as exports:
                    InstanceWasmMethods = 'InstanceWasmMethods :='
                    outfile.write(InstanceWasmMethods+"\n")
                    lines = exports.readlines()
                    for line in lines:
                        outfile.write("    "+line) # exports.txt
                with open("./dir/template/wasm3.dg", "rt") as wasm3:
                    outfile.write(wasm3.read())
        except Exception as e:
            print("[!] ERROR in make_template ./dir/template/..")
            print("[!]", e)

    def use_dharma(self, idx):
        try:
            # dharma로 js 생성
            cmd = []
            cmd.append("dharma")
            cmd.append("-grammars ./dir/template/dharma_template.dg")
            if idx == 0:
                cmd.append("-storage ./dir/input/")
            elif idx == 1:
                cmd.append("-storage ./dir/input2/")
            cmd.append("-format js")
            cmd.append("-count " + str(self.args.d))
            cmd = " ".join(cmd)
            print(cmd)
            subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True, shell=True, preexec_fn=os.setsid).wait()

        except Exception as e:
            print("[!] ERROR in use_dharma")
            print(e)


    def Make(self, idx, itr):
        self.use_wabt(itr)
        self.make_template()
        self.use_dharma(idx)