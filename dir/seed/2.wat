(module
  (type (;0;) (func))
  (type (;1;) (func (param i32) (result i32)))
  (func $__wasm_call_ctors (type 0))
  (func $malloc (type 1) (param i32) (result i32)
    (local i32)
    i32.const 0
    i32.const 0
    i32.load offset=1024
    local.tee 1
    local.get 0
    i32.add
    i32.store offset=1024
    local.get 1)
  (table (;0;) 1 1 funcref)
  (memory (;0;) 2)
  (global (;0;) (mut i32) (i32.const 66576))
  (global (;1;) i32 (i32.const 66576))
  (global (;2;) i32 (i32.const 1028))
  (global (;3;) i32 (i32.const 1024))
  (global (;4;) i32 (i32.const 1024))
  (export "memory" (memory 0))
  (export "__wasm_call_ctors" (func $__wasm_call_ctors))
  (export "__heap_base" (global 1))
  (export "__data_end" (global 2))
  (export "__dso_handle" (global 3))
  (export "malloc" (func $malloc))
  (export "bump_pointer" (global 4))
  (data (;0;) (i32.const 1024) "\10\04\01\00"))
