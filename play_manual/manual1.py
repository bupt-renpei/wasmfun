"""
Playing with WASM by manually writing it using our Python classes.

This is just a simple demo to demonstrate defining functions in WASM,
as well as importing functions from the host environment and using then
in WASM.
"""

import wasmfun as wf


root = wf.Module(
    wf.TypeSection(
        wf.FunctionSig(['f64']),  # import alert func
        wf.FunctionSig(['f64']),  # import write func (could share the sig)
        wf.FunctionSig(['f64', 'f64'], ['f64']), # add func
        wf.FunctionSig([]),  # start func
        ),
    wf.ImportSection(
        wf.Import('js', 'alert', 'function', 0),
        wf.Import('js', 'stdout_write', 'function', 1),
        ),
    wf.FunctionSection(2, 3),
    wf.ExportSection(
        wf.Export('add', 'function', 2),
        ),
    wf.StartSection(3),
    wf.CodeSection(
        wf.FunctionDef([], 
            ('f64.const', 42), ('call', 1),  # write 42
            # ('f64.const', 1337), ('call', 0),  # alert 1337
            ('get_local', 0), ('get_local', 1), ('f64.add'),
            ),
        wf.FunctionDef(['f64'],  # start func
            ('loop', 'emptyblock'),
                # write iter
                ('get_local', 0), ('call', 1),
                # Increase iter
                ('f64.const', 1), ('get_local', 0), ('f64.add'),
                ('tee_local', 0), ('f64.const', 10),
                ('f64.lt'), ('br_if', 0),
                ('end'),
            ),
        ),
    )


print(root)
root.show()

bb = root.to_binary()
print(bb)
wf.hexdump(bb)

wf.produce_example_html(__file__[:-3] + '.html', root.to_text(), bb)
