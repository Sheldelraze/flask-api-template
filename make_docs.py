from docs_generator import docs_helper

builder = docs_helper.DocsBuilder()

path = "service/sample_service.py"
with open("service/sample_service.py", "r") as fp:
    filename = path.split("/")[-1]
    script = fp.read()
    builder.extract(script, filename)
    builder.build()
