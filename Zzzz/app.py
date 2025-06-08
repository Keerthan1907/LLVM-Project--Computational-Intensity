from flask import Flask, request, render_template
import os
import subprocess
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
TEST_FOLDER = "tests"
BUILD_FOLDER = "build"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TEST_FOLDER, exist_ok=True)
os.makedirs(BUILD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
# def index():
#     output = ""

#     if request.method == "POST":
#         file = request.files["code_file"]
#         if file and file.filename.endswith(".c"):
#             # Save uploaded file
#             uid = str(uuid.uuid4())
#             c_path = os.path.join(TEST_FOLDER, f"{uid}.c")
#             ll_path = os.path.join(TEST_FOLDER, f"{uid}.ll")
#             file.save(c_path)

#             # Rebuild the .so plugin
#             build_command = (
#                 "clang++-15 -fPIC -shared -o build/ComputationalIntensityPass.so "
#                 "ComputationalIntensityPass.cpp "
#                 "`llvm-config-15 --cxxflags --ldflags --system-libs --libs core passes analysis support`"
#             )
#             try:
#                 subprocess.run(build_command, shell=True, check=True)
#             except subprocess.CalledProcessError:
#                 return render_template("upload.html", output="❌ Error building .so pass.")

#             # Step 1: Compile to LLVM IR (.ll)
#             try:
#                 subprocess.run(
#                     ["clang-15", "-S", "-emit-llvm", c_path, "-o", ll_path, "-O3"],
#                     check=True
#                 )
#             except subprocess.CalledProcessError:
#                 return render_template("index.html", output="❌ Error generating LLVM IR.")

#             # Step 2: Run the analysis pass
#             try:
#                 result = subprocess.run(
#                     [
#                         "/usr/lib/llvm-15/bin/opt",
#                         "-load-pass-plugin", "./build/ComputationalIntensityPass.so",
#                         "-passes=function(analyze-computational-intensity)",
#                         "-disable-output",
#                         ll_path
#                     ],
#                     capture_output=True,
#                     text=True,
#                     check=True
#                 )
#                 output = result.stderr
#             except subprocess.CalledProcessError as e:
#                 output = f"❌ Error running LLVM pass:\n{e.stderr}"

#     return render_template("upload.html", output=output)

# @app.route("/", methods=["GET", "POST"])
# def index():
#     output = ""

#     if request.method == "POST":
#         print("🔍 POST request received")
#         print("🧾 form keys:", request.form.keys())
#         print("📂 file keys:", request.files.keys())

#         if "code_file" not in request.files:
#             output = "❌ Error: 'code_file' not found in uploaded files."
#             return render_template("upload.html", output=output)

#         file = request.files["code_file"]

#         if file and file.filename.endswith(".c"):
#             uid = str(uuid.uuid4())
#             c_path = os.path.join(TEST_FOLDER, f"{uid}.c")
#             ll_path = os.path.join(TEST_FOLDER, f"{uid}.ll")
#             file.save(c_path)

#             build_command = (
#                 "clang++-15 -fPIC -shared -o build/ComputationalIntensityPass.so "
#                 "ComputationalIntensityPass.cpp "
#                 "`llvm-config-15 --cxxflags --ldflags --system-libs --libs core passes analysis support`"
#             )
#             try:
#                 subprocess.run(build_command, shell=True, check=True)
#             except subprocess.CalledProcessError:
#                 return render_template("upload.html", output="❌ Error building .so pass.")

#             try:
#                 subprocess.run(
#                     ["clang-15", "-S", "-emit-llvm", c_path, "-o", ll_path, "-O3"],
#                     check=True
#                 )
#             except subprocess.CalledProcessError:
#                 return render_template("upload.html", output="❌ Error generating LLVM IR.")

#             try:
#                 result = subprocess.run(
#                     [
#                         "/usr/lib/llvm-15/bin/opt",
#                         "-load-pass-plugin", "./build/ComputationalIntensityPass.so",
#                         "-passes=function(analyze-computational-intensity)",
#                         "-disable-output",
#                         ll_path
#                     ],
#                     capture_output=True,
#                     text=True,
#                     check=True
#                 )
#                 output = result.stderr
#             except subprocess.CalledProcessError as e:
#                 output = f"❌ Error running LLVM pass:\n{e.stderr}"

#     return render_template("upload.html", output=output)



@app.route("/", methods=["GET", "POST"])
def index():
    output = ""

    if request.method == "POST":
        print("🔍 POST request received")
        print("🧾 form keys:", request.form.keys())
        print("📂 file keys:", request.files.keys())

        if "code_file" not in request.files:
            output = "❌ Error: 'code_file' not found."
            return render_template("upload.html", output=output)

        file = request.files["code_file"]

        if file and file.filename.endswith(".c"):
            print("📁 Saving C file...")
            uid = str(uuid.uuid4())
            c_path = os.path.join(TEST_FOLDER, f"{uid}.c")
            ll_path = os.path.join(TEST_FOLDER, f"{uid}.ll")
            file.save(c_path)

            # Compile pass
            build_command = (
                "clang++-15 -fPIC -shared -o build/ComputationalIntensityPass.so "
                "ComputationalIntensityPass.cpp "
                "`llvm-config-15 --cxxflags --ldflags --system-libs --libs core passes analysis support`"
            )
            try:
                print("⚙️ Building LLVM pass...")
                subprocess.run(build_command, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                print("❌ Build error")
                return render_template("upload.html", output="❌ Error building .so pass.")

            try:
                print("🧬 Generating LLVM IR...")
                subprocess.run(
                    ["clang-15", "-S", "-emit-llvm", c_path, "-o", ll_path, "-O3"],
                    check=True
                )
            except subprocess.CalledProcessError as e:
                print("❌ LLVM IR generation failed")
                return render_template("upload.html", output="❌ Error generating LLVM IR.")

            try:
                print("🔍 Running LLVM pass...")
                result = subprocess.run(
                    [
                        "/usr/lib/llvm-15/bin/opt",
                        "-load-pass-plugin", "./build/ComputationalIntensityPass.so",
                        "-passes=function(analyze-computational-intensity)",
                        "-disable-output",
                        ll_path
                    ],
                    capture_output=True,
                    text=True,
                    check=True
                )
                output = result.stderr
                print("✅ Pass ran successfully!")
                print("🖨️ Output:\n", output)
            except subprocess.CalledProcessError as e:
                output = f"❌ Error running LLVM pass:\n{e.stderr}"
                print("❌ Error running pass:\n", e.stderr)

    return render_template("upload.html", output=output)

if __name__ == "__main__":
    app.run(debug=True)
