(module
  (type (;0;) (func))
  (type (;1;) (func (param i32) (result f32)))
  (type (;2;) (func (param i32) (result i32)))
  (func $__wasm_call_ctors (type 0))
  (func $hahaha (type 1) (param i32) (result f32)
    i32.const 0
    i32.load8_u offset=1024
    f32.convert_i32_u)
  (func $doubling (type 2) (param i32) (result i32)
    local.get 0
    i32.const 1
    i32.shl)
  (table (;0;) 1 1 funcref)
  (memory (;0;) 2)
  (global (;0;) (mut i32) (i32.const 66576))
  (global (;1;) i32 (i32.const 66576))
  (global (;2;) i32 (i32.const 1025))
  (global (;3;) i32 (i32.const 1024))
  (global (;4;) i32 (i32.const 1024))
  (export "memory" (memory 0))
  (export "__wasm_call_ctors" (func $__wasm_call_ctors))
  (export "__heap_base" (global 1))
  (export "__data_end" (global 2))
  (export "__dso_handle" (global 3))
  (export "hahaha" (func $hahaha))
  (export "doubling" (func $doubling))
  (export "aa" (global 4))
  (data (;0;) (i32.const 1024) "\ff"))
