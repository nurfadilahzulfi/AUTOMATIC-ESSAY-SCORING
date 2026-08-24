# Automatic Essay Scoring - Backend API

Sistem Backend REST API berbasis **Django** & **Django REST Framework (DRF)** yang dirancang untuk melakukan penilaian esai otomatis menggunakan kecerdasan buatan (**Ollama LLM - Llama 3.2:3b**) secara lokal. Sistem ini dilengkapi dengan modul **Zero Tolerance Proctoring** untuk mendeteksi kecurangan saat ujian berlangsung.

---

## Multi-Service Architecture

Proyek ini dibangun menggunakan arsitektur microservices terisolasi melalui **Docker Compose**:

1.  **`web`**: Django DRF Application server (berjalan di port `8000` internal, di-expose ke port **`8443`** host).
2.  **`db`**: PostgreSQL 15 sebagai database relasional utama.
3.  **`redis`**: Message broker untuk mendistribusikan antrean grading.
4.  **`celery`**: Worker asinkron yang memproses penilaian esai via LLM secara background.
5.  **`ollama`**: Server AI lokal tempat model LLM `llama3.2:3b` dieksekusi.

---

## STRUKTUR FOLDER
# Project Structure

```
AUTOMATIC-ESSAY-SCORING/
├── apps
│   ├── accounts
│   │   ├── migrations
│   │   │   ├── __init__.py
│   │   │   ├── 0001_initial.py
│   │   │   └── 0002_add_nip_field_for_dosen.py
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── exams
│   │   ├── migrations
│   │   │   ├── __init__.py
│   │   │   ├── 0001_initial.py
│   │   │   ├── 0002_rename_matapelajaran_relatedname_to_matakuliah.py
│   │   │   └── 0003_add_tahun_ajaran_to_ujian.py
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── grading
│   │   ├── migrations
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tasks.py
│   │   ├── tests.py
│   │   └── views.py
│   ├── proctoring
│   │   ├── migrations
│   │   │   ├── __init__.py
│   │   │   └── 0001_initial.py
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── reports
│   │   ├── migrations
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── submissions
│   │   ├── migrations
│   │   │   ├── __init__.py
│   │   │   └── 0001_initial.py
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   └── __init__.py
├── config
│   ├── __init__.py
│   ├── asgi.py
│   ├── celery.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── FINE-TUNING
│   ├── data
│   │   ├── cleaned_dataset.csv
│   │   ├── cleaned_dataset(1).csv
│   │   ├── cleaned_dataset(1)(1).csv
│   │   ├── cleaned_dataset(1)(2).csv
│   │   ├── Dataset Machine Learning.xlsx
│   │   ├── test.jsonl
│   │   ├── train.jsonl
│   │   └── val.jsonl
│   ├── outputs
│   │   ├── llama32_3b_aes_gguf
│   │   │   ├── chat_template.jinja
│   │   │   ├── config.json
│   │   │   ├── generation_config.json
│   │   │   ├── model-00001-of-00002.safetensors
│   │   │   ├── model-00002-of-00002.safetensors
│   │   │   ├── model.safetensors.index.json
│   │   │   ├── tokenizer_config.json
│   │   │   └── tokenizer.json
│   │   ├── llama32_3b_aes_gguf_gguf
│   │   │   ├── Llama-3.2-3B-Instruct.Q4_K_M.gguf
│   │   │   └── Modelfile
│   │   ├── llama32_3b_aes_lora
│   │   │   ├── checkpoint-114
│   │   │   │   ├── adapter_config.json
│   │   │   │   ├── adapter_model.safetensors
│   │   │   │   ├── chat_template.jinja
│   │   │   │   ├── optimizer.pt
│   │   │   │   ├── README.md
│   │   │   │   ├── rng_state.pth
│   │   │   │   ├── scheduler.pt
│   │   │   │   ├── tokenizer_config.json
│   │   │   │   ├── tokenizer.json
│   │   │   │   ├── trainer_state.json
│   │   │   │   └── training_args.bin
│   │   │   ├── checkpoint-38
│   │   │   │   ├── adapter_config.json
│   │   │   │   ├── adapter_model.safetensors
│   │   │   │   ├── chat_template.jinja
│   │   │   │   ├── optimizer.pt
│   │   │   │   ├── README.md
│   │   │   │   ├── rng_state.pth
│   │   │   │   ├── scheduler.pt
│   │   │   │   ├── tokenizer_config.json
│   │   │   │   ├── tokenizer.json
│   │   │   │   ├── trainer_state.json
│   │   │   │   └── training_args.bin
│   │   │   ├── checkpoint-76
│   │   │   │   ├── adapter_config.json
│   │   │   │   ├── adapter_model.safetensors
│   │   │   │   ├── chat_template.jinja
│   │   │   │   ├── optimizer.pt
│   │   │   │   ├── README.md
│   │   │   │   ├── rng_state.pth
│   │   │   │   ├── scheduler.pt
│   │   │   │   ├── tokenizer_config.json
│   │   │   │   ├── tokenizer.json
│   │   │   │   ├── trainer_state.json
│   │   │   │   └── training_args.bin
│   │   │   ├── adapter_config.json
│   │   │   ├── adapter_model.safetensors
│   │   │   ├── chat_template.jinja
│   │   │   ├── README.md
│   │   │   ├── tokenizer_config.json
│   │   │   └── tokenizer.json
│   │   ├── Qwen3-4B_gguf
│   │   │   ├── chat_template.jinja
│   │   │   ├── config.json
│   │   │   ├── generation_config.json
│   │   │   ├── model-00001-of-00002.safetensors
│   │   │   ├── model-00002-of-00002.safetensors
│   │   │   ├── model.safetensors.index.json
│   │   │   ├── tokenizer_config.json
│   │   │   └── tokenizer.json
│   │   ├── Qwen3-4B_gguf_gguf
│   │   │   ├── Modelfile
│   │   │   └── qwen3-4b.Q4_K_M.gguf
│   │   └── Qwen3-4B_lora
│   │       ├── checkpoint-114
│   │       │   ├── adapter_config.json
│   │       │   ├── adapter_model.safetensors
│   │       │   ├── chat_template.jinja
│   │       │   ├── optimizer.pt
│   │       │   ├── README.md
│   │       │   ├── rng_state.pth
│   │       │   ├── scheduler.pt
│   │       │   ├── tokenizer_config.json
│   │       │   ├── tokenizer.json
│   │       │   ├── trainer_state.json
│   │       │   └── training_args.bin
│   │       ├── checkpoint-38
│   │       │   ├── adapter_config.json
│   │       │   ├── adapter_model.safetensors
│   │       │   ├── chat_template.jinja
│   │       │   ├── optimizer.pt
│   │       │   ├── README.md
│   │       │   ├── rng_state.pth
│   │       │   ├── scheduler.pt
│   │       │   ├── tokenizer_config.json
│   │       │   ├── tokenizer.json
│   │       │   ├── trainer_state.json
│   │       │   └── training_args.bin
│   │       ├── checkpoint-76
│   │       │   ├── adapter_config.json
│   │       │   ├── adapter_model.safetensors
│   │       │   ├── chat_template.jinja
│   │       │   ├── optimizer.pt
│   │       │   ├── README.md
│   │       │   ├── rng_state.pth
│   │       │   ├── scheduler.pt
│   │       │   ├── tokenizer_config.json
│   │       │   ├── tokenizer.json
│   │       │   ├── trainer_state.json
│   │       │   └── training_args.bin
│   │       ├── adapter_config.json
│   │       ├── adapter_model.safetensors
│   │       ├── chat_template.jinja
│   │       ├── README.md
│   │       ├── tokenizer_config.json
│   │       └── tokenizer.json
│   ├── unsloth_compiled_cache
│   │   ├── moe_utils.py
│   │   ├── UnslothBCOTrainer.py
│   │   ├── UnslothCPOTrainer.py
│   │   ├── UnslothDPOTrainer.py
│   │   ├── UnslothGKDTrainer.py
│   │   ├── UnslothGRPOTrainer.py
│   │   ├── UnslothKTOTrainer.py
│   │   ├── UnslothNashMDTrainer.py
│   │   ├── UnslothOnlineDPOTrainer.py
│   │   ├── UnslothORPOTrainer.py
│   │   ├── UnslothPPOTrainer.py
│   │   ├── UnslothPRMTrainer.py
│   │   ├── UnslothRewardTrainer.py
│   │   ├── UnslothRLOOTrainer.py
│   │   ├── UnslothSFTTrainer.py
│   │   └── UnslothXPOTrainer.py
│   ├── venv
│   │   ├── etc
│   │   │   └── jupyter
│   │   │       ├── jupyter_notebook_config.d
│   │   │       │   └── jupyterlab.json
│   │   │       ├── jupyter_server_config.d
│   │   │       │   ├── jupyter_server_terminals.json
│   │   │       │   ├── jupyter-lsp-jupyter-server.json
│   │   │       │   ├── jupyterlab.json
│   │   │       │   ├── notebook_shim.json
│   │   │       │   └── notebook.json
│   │   │       └── nbconfig
│   │   │           └── notebook.d
│   │   ├── Include
│   │   ├── Lib
│   │   │   └── site-packages
│   │   │       ├── _argon2_cffi_bindings
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _ffi_build.py
│   │   │       │   └── _ffi.pyd
│   │   │       ├── _distutils_hack
│   │   │       │   ├── __init__.py
│   │   │       │   └── override.py
│   │   │       ├── _multiprocess
│   │   │       │   └── __init__.py
│   │   │       ├── _yaml
│   │   │       │   └── __init__.py
│   │   │       ├── ~-rch
│   │   │       │   ├── lib
│   │   │       │   └── _C.cp310-win_amd64.pyd
│   │   │       ├── ~~rch
│   │   │       │   ├── lib
│   │   │       │   └── _C.cp310-win_amd64.pyd
│   │   │       ├── ~arkupsafe
│   │   │       │   └── _speedups.cp310-win_amd64.pyd
│   │   │       ├── ~il
│   │   │       │   ├── _imaging.cp310-win_amd64.pyd
│   │   │       │   ├── _imagingft.cp310-win_amd64.pyd
│   │   │       │   └── _imagingmath.cp310-win_amd64.pyd
│   │   │       ├── ~orch
│   │   │       │   ├── lib
│   │   │       │   └── _C.cp310-win_amd64.pyd
│   │   │       ├── ~orchvision
│   │   │       │   ├── _C.pyd
│   │   │       │   ├── image.pyd
│   │   │       │   ├── jpeg8.dll
│   │   │       │   ├── libpng16.dll
│   │   │       │   ├── libsharpyuv.dll
│   │   │       │   ├── libwebp.dll
│   │   │       │   ├── nvjpeg64_12.dll
│   │   │       │   └── zlib.dll
│   │   │       ├── ~umpy
│   │   │       │   ├── _core
│   │   │       │   ├── fft
│   │   │       │   ├── linalg
│   │   │       │   └── random
│   │   │       ├── ~umpy.libs
│   │   │       │   ├── libscipy_openblas64_-13e2df515630b4a41f92893938845698.dll
│   │   │       │   └── msvcp140-263139962577ecda4cd9469ca360a746.dll
│   │   │       ├── accelerate
│   │   │       │   ├── commands
│   │   │       │   ├── test_utils
│   │   │       │   ├── utils
│   │   │       │   ├── __init__.py
│   │   │       │   ├── accelerator.py
│   │   │       │   ├── big_modeling.py
│   │   │       │   ├── checkpointing.py
│   │   │       │   ├── data_loader.py
│   │   │       │   ├── hooks.py
│   │   │       │   ├── inference.py
│   │   │       │   ├── launchers.py
│   │   │       │   ├── local_sgd.py
│   │   │       │   ├── logging.py
│   │   │       │   ├── memory_utils.py
│   │   │       │   ├── optimizer.py
│   │   │       │   ├── parallelism_config.py
│   │   │       │   ├── scheduler.py
│   │   │       │   ├── state.py
│   │   │       │   └── tracking.py
│   │   │       ├── accelerate-1.14.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── REQUESTED
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── aiohappyeyeballs
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _staggered.py
│   │   │       │   ├── impl.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── types.py
│   │   │       │   └── utils.py
│   │   │       ├── aiohappyeyeballs-2.7.1.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── aiohttp
│   │   │       │   ├── _websocket
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _cookie_helpers.py
│   │   │       │   ├── _cparser.pxd
│   │   │       │   ├── _find_header.pxd
│   │   │       │   ├── _headers.pxi
│   │   │       │   ├── _http_parser.cp310-win_amd64.pyd
│   │   │       │   ├── _http_parser.pyx
│   │   │       │   ├── _http_writer.cp310-win_amd64.pyd
│   │   │       │   ├── _http_writer.pyx
│   │   │       │   ├── abc.py
│   │   │       │   ├── base_protocol.py
│   │   │       │   ├── client_exceptions.py
│   │   │       │   ├── client_middleware_digest_auth.py
│   │   │       │   ├── client_middlewares.py
│   │   │       │   ├── client_proto.py
│   │   │       │   ├── client_reqrep.py
│   │   │       │   ├── client_ws.py
│   │   │       │   ├── client.py
│   │   │       │   ├── compression_utils.py
│   │   │       │   ├── connector.py
│   │   │       │   ├── cookiejar.py
│   │   │       │   ├── formdata.py
│   │   │       │   ├── hdrs.py
│   │   │       │   ├── helpers.py
│   │   │       │   ├── http_exceptions.py
│   │   │       │   ├── http_parser.py
│   │   │       │   ├── http_websocket.py
│   │   │       │   ├── http_writer.py
│   │   │       │   ├── http.py
│   │   │       │   ├── log.py
│   │   │       │   ├── multipart.py
│   │   │       │   ├── payload_streamer.py
│   │   │       │   ├── payload.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── pytest_plugin.py
│   │   │       │   ├── resolver.py
│   │   │       │   ├── streams.py
│   │   │       │   ├── tcp_helpers.py
│   │   │       │   ├── test_utils.py
│   │   │       │   ├── tracing.py
│   │   │       │   ├── typedefs.py
│   │   │       │   ├── web_app.py
│   │   │       │   ├── web_exceptions.py
│   │   │       │   ├── web_fileresponse.py
│   │   │       │   ├── web_log.py
│   │   │       │   ├── web_middlewares.py
│   │   │       │   ├── web_protocol.py
│   │   │       │   ├── web_request.py
│   │   │       │   ├── web_response.py
│   │   │       │   ├── web_routedef.py
│   │   │       │   ├── web_runner.py
│   │   │       │   ├── web_server.py
│   │   │       │   ├── web_urldispatcher.py
│   │   │       │   ├── web_ws.py
│   │   │       │   ├── web.py
│   │   │       │   └── worker.py
│   │   │       ├── aiohttp-3.14.3.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── aiosignal
│   │   │       │   ├── __init__.py
│   │   │       │   └── py.typed
│   │   │       ├── aiosignal-1.4.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── annotated_doc
│   │   │       │   ├── __init__.py
│   │   │       │   ├── main.py
│   │   │       │   └── py.typed
│   │   │       ├── annotated_doc-0.0.5.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── annotated_types
│   │   │       │   ├── __init__.py
│   │   │       │   ├── py.typed
│   │   │       │   └── test_cases.py
│   │   │       ├── annotated_types-0.8.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── anyio
│   │   │       │   ├── _backends
│   │   │       │   ├── _core
│   │   │       │   ├── abc
│   │   │       │   ├── streams
│   │   │       │   ├── __init__.py
│   │   │       │   ├── from_thread.py
│   │   │       │   ├── functools.py
│   │   │       │   ├── itertools.py
│   │   │       │   ├── lowlevel.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── pytest_plugin.py
│   │   │       │   ├── to_interpreter.py
│   │   │       │   ├── to_process.py
│   │   │       │   └── to_thread.py
│   │   │       ├── anyio-4.14.2.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── scm_file_list.json
│   │   │       │   ├── scm_version.json
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── argon2
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __main__.py
│   │   │       │   ├── _legacy.py
│   │   │       │   ├── _password_hasher.py
│   │   │       │   ├── _utils.py
│   │   │       │   ├── exceptions.py
│   │   │       │   ├── low_level.py
│   │   │       │   ├── profiles.py
│   │   │       │   └── py.typed
│   │   │       ├── argon2_cffi_bindings-25.1.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── argon2_cffi-25.1.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── arrow
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _version.py
│   │   │       │   ├── api.py
│   │   │       │   ├── arrow.py
│   │   │       │   ├── constants.py
│   │   │       │   ├── factory.py
│   │   │       │   ├── formatter.py
│   │   │       │   ├── locales.py
│   │   │       │   ├── parser.py
│   │   │       │   ├── py.typed
│   │   │       │   └── util.py
│   │   │       ├── arrow-1.4.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── asttokens
│   │   │       │   ├── __init__.py
│   │   │       │   ├── astroid_compat.py
│   │   │       │   ├── asttokens.py
│   │   │       │   ├── line_numbers.py
│   │   │       │   ├── mark_tokens.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── util.py
│   │   │       │   └── version.py
│   │   │       ├── asttokens-3.0.2.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── scm_file_list.json
│   │   │       │   ├── scm_version.json
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── async_lru
│   │   │       │   ├── __init__.py
│   │   │       │   └── py.typed
│   │   │       ├── async_lru-2.3.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── async_timeout
│   │   │       │   ├── __init__.py
│   │   │       │   └── py.typed
│   │   │       ├── async_timeout-5.0.1.dist-info
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   ├── WHEEL
│   │   │       │   └── zip-safe
│   │   │       ├── attr
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __init__.pyi
│   │   │       │   ├── _cmp.py
│   │   │       │   ├── _cmp.pyi
│   │   │       │   ├── _compat.py
│   │   │       │   ├── _config.py
│   │   │       │   ├── _funcs.py
│   │   │       │   ├── _make.py
│   │   │       │   ├── _next_gen.py
│   │   │       │   ├── _typing_compat.pyi
│   │   │       │   ├── _version_info.py
│   │   │       │   ├── _version_info.pyi
│   │   │       │   ├── converters.py
│   │   │       │   ├── converters.pyi
│   │   │       │   ├── exceptions.py
│   │   │       │   ├── exceptions.pyi
│   │   │       │   ├── filters.py
│   │   │       │   ├── filters.pyi
│   │   │       │   ├── py.typed
│   │   │       │   ├── setters.py
│   │   │       │   ├── setters.pyi
│   │   │       │   ├── validators.py
│   │   │       │   └── validators.pyi
│   │   │       ├── attrs
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __init__.pyi
│   │   │       │   ├── converters.py
│   │   │       │   ├── exceptions.py
│   │   │       │   ├── filters.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── setters.py
│   │   │       │   └── validators.py
│   │   │       ├── attrs-26.1.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── babel
│   │   │       │   ├── locale-data
│   │   │       │   ├── localtime
│   │   │       │   ├── messages
│   │   │       │   ├── __init__.py
│   │   │       │   ├── core.py
│   │   │       │   ├── dates.py
│   │   │       │   ├── global.dat
│   │   │       │   ├── languages.py
│   │   │       │   ├── lists.py
│   │   │       │   ├── localedata.py
│   │   │       │   ├── numbers.py
│   │   │       │   ├── plural.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── support.py
│   │   │       │   ├── units.py
│   │   │       │   └── util.py
│   │   │       ├── babel-2.18.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── beautifulsoup4-4.15.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── bitsandbytes
│   │   │       │   ├── autograd
│   │   │       │   ├── backends
│   │   │       │   ├── diagnostics
│   │   │       │   ├── nn
│   │   │       │   ├── optim
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __main__.py
│   │   │       │   ├── _ops.py
│   │   │       │   ├── cextension.py
│   │   │       │   ├── consts.py
│   │   │       │   ├── cuda_specs.py
│   │   │       │   ├── functional.py
│   │   │       │   ├── libbitsandbytes_cpu.dll
│   │   │       │   ├── libbitsandbytes_cuda118.dll
│   │   │       │   ├── libbitsandbytes_cuda121.dll
│   │   │       │   ├── libbitsandbytes_cuda124.dll
│   │   │       │   ├── libbitsandbytes_cuda126.dll
│   │   │       │   ├── libbitsandbytes_cuda128.dll
│   │   │       │   ├── libbitsandbytes_cuda130.dll
│   │   │       │   ├── libbitsandbytes_cuda132.dll
│   │   │       │   ├── libbitsandbytes_rocm714.dll
│   │   │       │   ├── libbitsandbytes_rocm72.dll
│   │   │       │   ├── libbitsandbytes_xpu2025.dll
│   │   │       │   ├── libbitsandbytes_xpu2026.dll
│   │   │       │   ├── py.typed
│   │   │       │   └── utils.py
│   │   │       ├── bitsandbytes-0.50.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── REQUESTED
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── bleach
│   │   │       │   ├── _vendor
│   │   │       │   ├── __init__.py
│   │   │       │   ├── callbacks.py
│   │   │       │   ├── css_sanitizer.py
│   │   │       │   ├── html5lib_shim.py
│   │   │       │   ├── linkifier.py
│   │   │       │   ├── parse_shim.py
│   │   │       │   ├── sanitizer.py
│   │   │       │   └── six_shim.py
│   │   │       ├── bleach-6.4.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── bs4
│   │   │       │   ├── builder
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _deprecation.py
│   │   │       │   ├── _typing.py
│   │   │       │   ├── _warnings.py
│   │   │       │   ├── css.py
│   │   │       │   ├── dammit.py
│   │   │       │   ├── diagnose.py
│   │   │       │   ├── element.py
│   │   │       │   ├── exceptions.py
│   │   │       │   ├── filter.py
│   │   │       │   ├── formatter.py
│   │   │       │   └── py.typed
│   │   │       ├── certifi
│   │   │       │   ├── tests
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __main__.py
│   │   │       │   ├── cacert.pem
│   │   │       │   ├── core.py
│   │   │       │   └── py.typed
│   │   │       ├── certifi-2026.7.22.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── cffi
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _cffi_errors.h
│   │   │       │   ├── _cffi_gen_src.py
│   │   │       │   ├── _cffi_include.h
│   │   │       │   ├── _embedding.h
│   │   │       │   ├── _imp_emulation.py
│   │   │       │   ├── _shimmed_dist_utils.py
│   │   │       │   ├── api.py
│   │   │       │   ├── backend_ctypes.py
│   │   │       │   ├── cffi_opcode.py
│   │   │       │   ├── commontypes.py
│   │   │       │   ├── cparser.py
│   │   │       │   ├── error.py
│   │   │       │   ├── ffiplatform.py
│   │   │       │   ├── gen_src.py
│   │   │       │   ├── lock.py
│   │   │       │   ├── model.py
│   │   │       │   ├── parse_c_type.h
│   │   │       │   ├── pkgconfig.py
│   │   │       │   ├── recompiler.py
│   │   │       │   ├── setuptools_ext.py
│   │   │       │   ├── vengine_cpy.py
│   │   │       │   ├── vengine_gen.py
│   │   │       │   └── verifier.py
│   │   │       ├── cffi-2.1.1.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── charset_normalizer
│   │   │       │   ├── cli
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __main__.py
│   │   │       │   ├── api.py
│   │   │       │   ├── cd.cp310-win_amd64.pyd
│   │   │       │   ├── cd.py
│   │   │       │   ├── constant.py
│   │   │       │   ├── legacy.py
│   │   │       │   ├── md.cp310-win_amd64.pyd
│   │   │       │   ├── md.py
│   │   │       │   ├── models.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── utils.py
│   │   │       │   └── version.py
│   │   │       ├── charset_normalizer-3.4.9.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── click
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _compat.py
│   │   │       │   ├── _termui_impl.py
│   │   │       │   ├── _textwrap.py
│   │   │       │   ├── _utils.py
│   │   │       │   ├── _winconsole.py
│   │   │       │   ├── core.py
│   │   │       │   ├── decorators.py
│   │   │       │   ├── exceptions.py
│   │   │       │   ├── formatting.py
│   │   │       │   ├── globals.py
│   │   │       │   ├── parser.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── shell_completion.py
│   │   │       │   ├── termui.py
│   │   │       │   ├── testing.py
│   │   │       │   ├── types.py
│   │   │       │   └── utils.py
│   │   │       ├── click-8.4.2.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── colorama
│   │   │       │   ├── tests
│   │   │       │   ├── __init__.py
│   │   │       │   ├── ansi.py
│   │   │       │   ├── ansitowin32.py
│   │   │       │   ├── initialise.py
│   │   │       │   ├── win32.py
│   │   │       │   └── winterm.py
│   │   │       ├── colorama-0.4.6.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── comm
│   │   │       │   ├── __init__.py
│   │   │       │   ├── base_comm.py
│   │   │       │   └── py.typed
│   │   │       ├── comm-0.2.3.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── contourpy
│   │   │       │   ├── util
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _contourpy.cp310-win_amd64.lib
│   │   │       │   ├── _contourpy.cp310-win_amd64.pyd
│   │   │       │   ├── _contourpy.pyi
│   │   │       │   ├── _version.py
│   │   │       │   ├── array.py
│   │   │       │   ├── chunk.py
│   │   │       │   ├── convert.py
│   │   │       │   ├── dechunk.py
│   │   │       │   ├── enum_util.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── typecheck.py
│   │   │       │   └── types.py
│   │   │       ├── contourpy-1.3.2.dist-info
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── cut_cross_entropy
│   │   │       │   ├── __init__.py
│   │   │       │   ├── cce_backward.py
│   │   │       │   ├── cce_lse_forward.py
│   │   │       │   ├── cce.py
│   │   │       │   ├── constants.py
│   │   │       │   ├── doc.py
│   │   │       │   ├── indexed_dot.py
│   │   │       │   ├── linear_cross_entropy.py
│   │   │       │   ├── tl_autotune.py
│   │   │       │   ├── tl_utils.py
│   │   │       │   ├── torch_compile.py
│   │   │       │   └── utils.py
│   │   │       ├── cut_cross_entropy-25.1.1.dist-info
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── cycler
│   │   │       │   ├── __init__.py
│   │   │       │   └── py.typed
│   │   │       ├── cycler-0.12.1.dist-info
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── datasets
│   │   │       │   ├── commands
│   │   │       │   ├── download
│   │   │       │   ├── features
│   │   │       │   ├── filesystems
│   │   │       │   ├── formatting
│   │   │       │   ├── io
│   │   │       │   ├── packaged_modules
│   │   │       │   ├── parallel
│   │   │       │   ├── utils
│   │   │       │   ├── __init__.py
│   │   │       │   ├── arrow_dataset.py
│   │   │       │   ├── arrow_reader.py
│   │   │       │   ├── arrow_writer.py
│   │   │       │   ├── builder.py
│   │   │       │   ├── combine.py
│   │   │       │   ├── config.py
│   │   │       │   ├── data_files.py
│   │   │       │   ├── dataset_dict.py
│   │   │       │   ├── distributed.py
│   │   │       │   ├── exceptions.py
│   │   │       │   ├── fingerprint.py
│   │   │       │   ├── hub.py
│   │   │       │   ├── info.py
│   │   │       │   ├── inspect.py
│   │   │       │   ├── iterable_dataset.py
│   │   │       │   ├── keyhash.py
│   │   │       │   ├── load.py
│   │   │       │   ├── naming.py
│   │   │       │   ├── search.py
│   │   │       │   ├── splits.py
│   │   │       │   ├── streaming.py
│   │   │       │   └── table.py
│   │   │       ├── datasets-4.3.0.dist-info
│   │   │       │   ├── AUTHORS
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── REQUESTED
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── dateutil
│   │   │       │   ├── parser
│   │   │       │   ├── tz
│   │   │       │   ├── zoneinfo
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _common.py
│   │   │       │   ├── _version.py
│   │   │       │   ├── easter.py
│   │   │       │   ├── relativedelta.py
│   │   │       │   ├── rrule.py
│   │   │       │   ├── tzwin.py
│   │   │       │   └── utils.py
│   │   │       ├── debugpy
│   │   │       │   ├── _vendored
│   │   │       │   ├── adapter
│   │   │       │   ├── common
│   │   │       │   ├── launcher
│   │   │       │   ├── server
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __main__.py
│   │   │       │   ├── _version.py
│   │   │       │   ├── public_api.py
│   │   │       │   ├── py.typed
│   │   │       │   └── ThirdPartyNotices.txt
│   │   │       ├── debugpy-1.8.21.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── decorator
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __init__.pyi
│   │   │       │   └── py.typed
│   │   │       ├── decorator-5.3.1.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── defusedxml
│   │   │       │   ├── __init__.py
│   │   │       │   ├── cElementTree.py
│   │   │       │   ├── common.py
│   │   │       │   ├── ElementTree.py
│   │   │       │   ├── expatbuilder.py
│   │   │       │   ├── expatreader.py
│   │   │       │   ├── lxml.py
│   │   │       │   ├── minidom.py
│   │   │       │   ├── pulldom.py
│   │   │       │   ├── sax.py
│   │   │       │   └── xmlrpc.py
│   │   │       ├── defusedxml-0.7.1.dist-info
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── diffusers
│   │   │       │   ├── commands
│   │   │       │   ├── experimental
│   │   │       │   ├── guiders
│   │   │       │   ├── hooks
│   │   │       │   ├── loaders
│   │   │       │   ├── models
│   │   │       │   ├── modular_pipelines
│   │   │       │   ├── pipelines
│   │   │       │   ├── quantizers
│   │   │       │   ├── schedulers
│   │   │       │   ├── utils
│   │   │       │   ├── __init__.py
│   │   │       │   ├── callbacks.py
│   │   │       │   ├── configuration_utils.py
│   │   │       │   ├── dependency_versions_check.py
│   │   │       │   ├── dependency_versions_table.py
│   │   │       │   ├── image_processor.py
│   │   │       │   ├── optimization.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── training_utils.py
│   │   │       │   └── video_processor.py
│   │   │       ├── diffusers-0.39.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── dill
│   │   │       │   ├── tests
│   │   │       │   ├── __diff.py
│   │   │       │   ├── __info__.py
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _dill.py
│   │   │       │   ├── _objects.py
│   │   │       │   ├── _shims.py
│   │   │       │   ├── detect.py
│   │   │       │   ├── logger.py
│   │   │       │   ├── objtypes.py
│   │   │       │   ├── pointers.py
│   │   │       │   ├── session.py
│   │   │       │   ├── settings.py
│   │   │       │   ├── source.py
│   │   │       │   └── temp.py
│   │   │       ├── dill-0.4.0.dist-info
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── docstring_parser
│   │   │       │   ├── __init__.py
│   │   │       │   ├── attrdoc.py
│   │   │       │   ├── common.py
│   │   │       │   ├── epydoc.py
│   │   │       │   ├── google.py
│   │   │       │   ├── numpydoc.py
│   │   │       │   ├── parser.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── rest.py
│   │   │       │   └── util.py
│   │   │       ├── docstring_parser-0.18.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── downward
│   │   │       │   ├── parsers
│   │   │       │   ├── reports
│   │   │       │   ├── __init__.py
│   │   │       │   ├── cached_revision.py
│   │   │       │   ├── experiment.py
│   │   │       │   ├── outcomes.py
│   │   │       │   └── suites.py
│   │   │       ├── et_xmlfile
│   │   │       │   ├── __init__.py
│   │   │       │   ├── incremental_tree.py
│   │   │       │   └── xmlfile.py
│   │   │       ├── et_xmlfile-2.0.0.dist-info
│   │   │       │   ├── AUTHORS.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENCE.python
│   │   │       │   ├── LICENCE.rst
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── exceptiongroup
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _catch.py
│   │   │       │   ├── _exceptions.py
│   │   │       │   ├── _formatting.py
│   │   │       │   ├── _suppress.py
│   │   │       │   ├── _version.py
│   │   │       │   └── py.typed
│   │   │       ├── exceptiongroup-1.3.1.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── executing
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _exceptions.py
│   │   │       │   ├── _position_node_finder.py
│   │   │       │   ├── _pytest_utils.py
│   │   │       │   ├── _utils.py
│   │   │       │   ├── executing.py
│   │   │       │   ├── py.typed
│   │   │       │   └── version.py
│   │   │       ├── executing-2.2.1.dist-info
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE.txt
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── fastjsonschema
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __main__.py
│   │   │       │   ├── draft04.py
│   │   │       │   ├── draft06.py
│   │   │       │   ├── draft07.py
│   │   │       │   ├── draft2019.py
│   │   │       │   ├── exceptions.py
│   │   │       │   ├── generator.py
│   │   │       │   ├── indent.py
│   │   │       │   ├── ref_resolver.py
│   │   │       │   └── version.py
│   │   │       ├── fastjsonschema-2.22.1.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── filelock
│   │   │       │   ├── _soft_rw
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _api.py
│   │   │       │   ├── _async_read_write.py
│   │   │       │   ├── _error.py
│   │   │       │   ├── _read_write.py
│   │   │       │   ├── _soft.py
│   │   │       │   ├── _unix.py
│   │   │       │   ├── _util.py
│   │   │       │   ├── _windows.py
│   │   │       │   ├── asyncio.py
│   │   │       │   ├── py.typed
│   │   │       │   └── version.py
│   │   │       ├── filelock-3.29.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── fontTools
│   │   │       │   ├── cffLib
│   │   │       │   ├── colorLib
│   │   │       │   ├── config
│   │   │       │   ├── cu2qu
│   │   │       │   ├── designspaceLib
│   │   │       │   ├── diff
│   │   │       │   ├── encodings
│   │   │       │   ├── feaLib
│   │   │       │   ├── merge
│   │   │       │   ├── misc
│   │   │       │   ├── mtiLib
│   │   │       │   ├── otlLib
│   │   │       │   ├── pens
│   │   │       │   ├── qu2cu
│   │   │       │   ├── subset
│   │   │       │   ├── svgLib
│   │   │       │   ├── t1Lib
│   │   │       │   ├── ttLib
│   │   │       │   ├── ufoLib
│   │   │       │   ├── unicodedata
│   │   │       │   ├── varLib
│   │   │       │   ├── voltLib
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __main__.py
│   │   │       │   ├── afmLib.py
│   │   │       │   ├── agl.py
│   │   │       │   ├── annotations.py
│   │   │       │   ├── fontBuilder.py
│   │   │       │   ├── help.py
│   │   │       │   ├── tfmLib.py
│   │   │       │   ├── ttx.py
│   │   │       │   └── unicode.py
│   │   │       ├── fonttools-4.63.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── fqdn
│   │   │       │   ├── __init__.py
│   │   │       │   └── _compat.py
│   │   │       ├── fqdn-1.5.1.dist-info
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   ├── WHEEL
│   │   │       │   └── zip-safe
│   │   │       ├── frozenlist
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __init__.pyi
│   │   │       │   ├── _frozenlist.cp310-win_amd64.pyd
│   │   │       │   ├── _frozenlist.pyx
│   │   │       │   └── py.typed
│   │   │       ├── frozenlist-1.8.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── fsspec
│   │   │       │   ├── implementations
│   │   │       │   ├── tests
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _version.py
│   │   │       │   ├── archive.py
│   │   │       │   ├── asyn.py
│   │   │       │   ├── caching.py
│   │   │       │   ├── callbacks.py
│   │   │       │   ├── compression.py
│   │   │       │   ├── config.py
│   │   │       │   ├── conftest.py
│   │   │       │   ├── core.py
│   │   │       │   ├── dircache.py
│   │   │       │   ├── exceptions.py
│   │   │       │   ├── fuse.py
│   │   │       │   ├── generic.py
│   │   │       │   ├── gui.py
│   │   │       │   ├── json.py
│   │   │       │   ├── mapping.py
│   │   │       │   ├── parquet.py
│   │   │       │   ├── registry.py
│   │   │       │   ├── spec.py
│   │   │       │   ├── transaction.py
│   │   │       │   └── utils.py
│   │   │       ├── fsspec-2025.9.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── functorch
│   │   │       │   ├── _src
│   │   │       │   ├── compile
│   │   │       │   ├── dim
│   │   │       │   ├── einops
│   │   │       │   ├── experimental
│   │   │       │   └── __init__.py
│   │   │       ├── gguf
│   │   │       │   ├── scripts
│   │   │       │   ├── __init__.py
│   │   │       │   ├── constants.py
│   │   │       │   ├── gguf_reader.py
│   │   │       │   ├── gguf_writer.py
│   │   │       │   ├── gguf.py
│   │   │       │   ├── lazy.py
│   │   │       │   ├── metadata.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── quants.py
│   │   │       │   ├── tensor_mapping.py
│   │   │       │   ├── utility.py
│   │   │       │   └── vocab.py
│   │   │       ├── gguf-0.19.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── REQUESTED
│   │   │       │   └── WHEEL
│   │   │       ├── google
│   │   │       │   ├── _upb
│   │   │       │   └── protobuf
│   │   │       ├── h11
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _abnf.py
│   │   │       │   ├── _connection.py
│   │   │       │   ├── _events.py
│   │   │       │   ├── _headers.py
│   │   │       │   ├── _readers.py
│   │   │       │   ├── _receivebuffer.py
│   │   │       │   ├── _state.py
│   │   │       │   ├── _util.py
│   │   │       │   ├── _version.py
│   │   │       │   ├── _writers.py
│   │   │       │   └── py.typed
│   │   │       ├── h11-0.16.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── hf_transfer
│   │   │       │   ├── __init__.py
│   │   │       │   └── hf_transfer.pyd
│   │   │       ├── hf_transfer-0.1.9.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── hf_xet
│   │   │       │   ├── __init__.py
│   │   │       │   └── hf_xet.pyd
│   │   │       ├── hf_xet-1.6.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── sboms
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── httpcore
│   │   │       │   ├── _async
│   │   │       │   ├── _backends
│   │   │       │   ├── _sync
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _api.py
│   │   │       │   ├── _exceptions.py
│   │   │       │   ├── _models.py
│   │   │       │   ├── _ssl.py
│   │   │       │   ├── _synchronization.py
│   │   │       │   ├── _trace.py
│   │   │       │   ├── _utils.py
│   │   │       │   └── py.typed
│   │   │       ├── httpcore-1.0.9.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── httpx
│   │   │       │   ├── _transports
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __version__.py
│   │   │       │   ├── _api.py
│   │   │       │   ├── _auth.py
│   │   │       │   ├── _client.py
│   │   │       │   ├── _config.py
│   │   │       │   ├── _content.py
│   │   │       │   ├── _decoders.py
│   │   │       │   ├── _exceptions.py
│   │   │       │   ├── _main.py
│   │   │       │   ├── _models.py
│   │   │       │   ├── _multipart.py
│   │   │       │   ├── _status_codes.py
│   │   │       │   ├── _types.py
│   │   │       │   ├── _urlparse.py
│   │   │       │   ├── _urls.py
│   │   │       │   ├── _utils.py
│   │   │       │   └── py.typed
│   │   │       ├── httpx-0.28.1.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── huggingface_hub
│   │   │       │   ├── _hot_reload
│   │   │       │   ├── cli
│   │   │       │   ├── inference
│   │   │       │   ├── serialization
│   │   │       │   ├── templates
│   │   │       │   ├── utils
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _buckets.py
│   │   │       │   ├── _commit_api.py
│   │   │       │   ├── _commit_scheduler.py
│   │   │       │   ├── _dataset_viewer.py
│   │   │       │   ├── _eval_results.py
│   │   │       │   ├── _inference_endpoints.py
│   │   │       │   ├── _jobs_api.py
│   │   │       │   ├── _local_folder.py
│   │   │       │   ├── _login.py
│   │   │       │   ├── _oauth.py
│   │   │       │   ├── _oidc.py
│   │   │       │   ├── _revision.py
│   │   │       │   ├── _sandbox_cache.py
│   │   │       │   ├── _sandbox.py
│   │   │       │   ├── _snapshot_download.py
│   │   │       │   ├── _space_api.py
│   │   │       │   ├── _tensorboard_logger.py
│   │   │       │   ├── _tree_cache.py
│   │   │       │   ├── _upload_large_folder.py
│   │   │       │   ├── _upload_pipeline.py
│   │   │       │   ├── _webhooks_payload.py
│   │   │       │   ├── _webhooks_server.py
│   │   │       │   ├── community.py
│   │   │       │   ├── constants.py
│   │   │       │   ├── dataclasses.py
│   │   │       │   ├── errors.py
│   │   │       │   ├── fastai_utils.py
│   │   │       │   ├── file_download.py
│   │   │       │   ├── hf_api.py
│   │   │       │   ├── hf_file_system.py
│   │   │       │   ├── hub_mixin.py
│   │   │       │   ├── lfs.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── repocard_data.py
│   │   │       │   └── repocard.py
│   │   │       ├── huggingface_hub-1.26.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── idna
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __main__.py
│   │   │       │   ├── cli.py
│   │   │       │   ├── codec.py
│   │   │       │   ├── compat.py
│   │   │       │   ├── core.py
│   │   │       │   ├── idnadata.py
│   │   │       │   ├── intranges.py
│   │   │       │   ├── package_data.py
│   │   │       │   ├── py.typed
│   │   │       │   └── uts46data.py
│   │   │       ├── idna-3.18.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── importlib_metadata
│   │   │       │   ├── compat
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _adapters.py
│   │   │       │   ├── _collections.py
│   │   │       │   ├── _compat.py
│   │   │       │   ├── _context.py
│   │   │       │   ├── _functools.py
│   │   │       │   ├── _itertools.py
│   │   │       │   ├── _meta.py
│   │   │       │   ├── _text.py
│   │   │       │   ├── diagnose.py
│   │   │       │   └── py.typed
│   │   │       ├── importlib_metadata-9.0.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── ipykernel
│   │   │       │   ├── comm
│   │   │       │   ├── gui
│   │   │       │   ├── inprocess
│   │   │       │   ├── pylab
│   │   │       │   ├── resources
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __main__.py
│   │   │       │   ├── _eventloop_macos.py
│   │   │       │   ├── _version.py
│   │   │       │   ├── compiler.py
│   │   │       │   ├── connect.py
│   │   │       │   ├── control.py
│   │   │       │   ├── debugger.py
│   │   │       │   ├── displayhook.py
│   │   │       │   ├── embed.py
│   │   │       │   ├── eventloops.py
│   │   │       │   ├── heartbeat.py
│   │   │       │   ├── iostream.py
│   │   │       │   ├── ipkernel.py
│   │   │       │   ├── jsonutil.py
│   │   │       │   ├── kernelapp.py
│   │   │       │   ├── kernelbase.py
│   │   │       │   ├── kernelspec.py
│   │   │       │   ├── log.py
│   │   │       │   ├── parentpoller.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── shellchannel.py
│   │   │       │   ├── socket_pair.py
│   │   │       │   ├── subshell_manager.py
│   │   │       │   ├── subshell.py
│   │   │       │   ├── thread.py
│   │   │       │   ├── trio_runner.py
│   │   │       │   ├── utils.py
│   │   │       │   └── zmqshell.py
│   │   │       ├── ipykernel-7.3.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── IPython
│   │   │       │   ├── core
│   │   │       │   ├── extensions
│   │   │       │   ├── external
│   │   │       │   ├── lib
│   │   │       │   ├── sphinxext
│   │   │       │   ├── terminal
│   │   │       │   ├── testing
│   │   │       │   ├── utils
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __main__.py
│   │   │       │   ├── conftest.py
│   │   │       │   ├── consoleapp.py
│   │   │       │   ├── display.py
│   │   │       │   ├── paths.py
│   │   │       │   └── py.typed
│   │   │       ├── ipython-8.39.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── ipywidgets
│   │   │       │   ├── tests
│   │   │       │   ├── widgets
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _version.py
│   │   │       │   ├── comm.py
│   │   │       │   ├── embed.py
│   │   │       │   ├── state.schema.json
│   │   │       │   └── view.schema.json
│   │   │       ├── ipywidgets-8.1.8.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── isoduration
│   │   │       │   ├── formatter
│   │   │       │   ├── operations
│   │   │       │   ├── parser
│   │   │       │   ├── __init__.py
│   │   │       │   ├── constants.py
│   │   │       │   └── types.py
│   │   │       ├── isoduration-20.11.0.dist-info
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── jedi
│   │   │       │   ├── api
│   │   │       │   ├── inference
│   │   │       │   ├── plugins
│   │   │       │   ├── third_party
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __main__.py
│   │   │       │   ├── _compatibility.py
│   │   │       │   ├── cache.py
│   │   │       │   ├── common.py
│   │   │       │   ├── debug.py
│   │   │       │   ├── file_io.py
│   │   │       │   ├── parser_utils.py
│   │   │       │   ├── settings.py
│   │   │       │   └── utils.py
│   │   │       ├── jedi-0.20.0.dist-info
│   │   │       │   ├── AUTHORS.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE.txt
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── jinja2
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _identifier.py
│   │   │       │   ├── async_utils.py
│   │   │       │   ├── bccache.py
│   │   │       │   ├── compiler.py
│   │   │       │   ├── constants.py
│   │   │       │   ├── debug.py
│   │   │       │   ├── defaults.py
│   │   │       │   ├── environment.py
│   │   │       │   ├── exceptions.py
│   │   │       │   ├── ext.py
│   │   │       │   ├── filters.py
│   │   │       │   ├── idtracking.py
│   │   │       │   ├── lexer.py
│   │   │       │   ├── loaders.py
│   │   │       │   ├── meta.py
│   │   │       │   ├── nativetypes.py
│   │   │       │   ├── nodes.py
│   │   │       │   ├── optimizer.py
│   │   │       │   ├── parser.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── runtime.py
│   │   │       │   ├── sandbox.py
│   │   │       │   ├── tests.py
│   │   │       │   ├── utils.py
│   │   │       │   └── visitor.py
│   │   │       ├── jinja2-3.1.6.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── joblib
│   │   │       │   ├── externals
│   │   │       │   ├── test
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _cloudpickle_wrapper.py
│   │   │       │   ├── _dask.py
│   │   │       │   ├── _memmapping_reducer.py
│   │   │       │   ├── _multiprocessing_helpers.py
│   │   │       │   ├── _parallel_backends.py
│   │   │       │   ├── _store_backends.py
│   │   │       │   ├── _utils.py
│   │   │       │   ├── backports.py
│   │   │       │   ├── compressor.py
│   │   │       │   ├── disk.py
│   │   │       │   ├── executor.py
│   │   │       │   ├── func_inspect.py
│   │   │       │   ├── hashing.py
│   │   │       │   ├── logger.py
│   │   │       │   ├── memory.py
│   │   │       │   ├── numpy_pickle_compat.py
│   │   │       │   ├── numpy_pickle_utils.py
│   │   │       │   ├── numpy_pickle.py
│   │   │       │   ├── parallel.py
│   │   │       │   ├── pool.py
│   │   │       │   └── testing.py
│   │   │       ├── joblib-1.5.3.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── json5
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __main__.py
│   │   │       │   ├── host.py
│   │   │       │   ├── lib.py
│   │   │       │   ├── parser.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── tool.py
│   │   │       │   └── version.py
│   │   │       ├── json5-0.15.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── jsonpointer-3.1.1.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── jsonschema
│   │   │       │   ├── benchmarks
│   │   │       │   ├── tests
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __main__.py
│   │   │       │   ├── _format.py
│   │   │       │   ├── _keywords.py
│   │   │       │   ├── _legacy_keywords.py
│   │   │       │   ├── _types.py
│   │   │       │   ├── _typing.py
│   │   │       │   ├── _utils.py
│   │   │       │   ├── cli.py
│   │   │       │   ├── exceptions.py
│   │   │       │   ├── protocols.py
│   │   │       │   └── validators.py
│   │   │       ├── jsonschema_specifications
│   │   │       │   ├── schemas
│   │   │       │   ├── tests
│   │   │       │   ├── __init__.py
│   │   │       │   └── _core.py
│   │   │       ├── jsonschema_specifications-2025.9.1.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── jsonschema-4.26.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── jupyter_builder
│   │   │       │   ├── extension_commands
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _version.py
│   │   │       │   ├── base_extension_app.py
│   │   │       │   ├── commands.py
│   │   │       │   ├── constants.py
│   │   │       │   ├── core_path.py
│   │   │       │   ├── debug_log_file_mixin.py
│   │   │       │   ├── federated_extensions_requirements.py
│   │   │       │   ├── federated_extensions.py
│   │   │       │   ├── jlpm.py
│   │   │       │   ├── jupyterlab_semver.py
│   │   │       │   ├── main.py
│   │   │       │   ├── py.typed
│   │   │       │   └── yarn.js
│   │   │       ├── jupyter_builder-1.2.1.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── jupyter_client
│   │   │       │   ├── asynchronous
│   │   │       │   ├── blocking
│   │   │       │   ├── ioloop
│   │   │       │   ├── provisioning
│   │   │       │   ├── ssh
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _version.py
│   │   │       │   ├── adapter.py
│   │   │       │   ├── channels.py
│   │   │       │   ├── channelsabc.py
│   │   │       │   ├── client.py
│   │   │       │   ├── clientabc.py
│   │   │       │   ├── connect.py
│   │   │       │   ├── consoleapp.py
│   │   │       │   ├── jsonutil.py
│   │   │       │   ├── kernelapp.py
│   │   │       │   ├── kernelspec.py
│   │   │       │   ├── kernelspecapp.py
│   │   │       │   ├── launcher.py
│   │   │       │   ├── localinterfaces.py
│   │   │       │   ├── manager.py
│   │   │       │   ├── managerabc.py
│   │   │       │   ├── multikernelmanager.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── restarter.py
│   │   │       │   ├── runapp.py
│   │   │       │   ├── session.py
│   │   │       │   ├── threaded.py
│   │   │       │   ├── utils.py
│   │   │       │   └── win_interrupt.py
│   │   │       ├── jupyter_client-8.9.1.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── jupyter_console
│   │   │       │   ├── tests
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __main__.py
│   │   │       │   ├── _version.py
│   │   │       │   ├── app.py
│   │   │       │   ├── completer.py
│   │   │       │   ├── ptshell.py
│   │   │       │   ├── utils.py
│   │   │       │   └── zmqhistory.py
│   │   │       ├── jupyter_console-6.6.3.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── jupyter_core
│   │   │       │   ├── utils
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __main__.py
│   │   │       │   ├── application.py
│   │   │       │   ├── command.py
│   │   │       │   ├── migrate.py
│   │   │       │   ├── paths.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── troubleshoot.py
│   │   │       │   └── version.py
│   │   │       ├── jupyter_core-5.9.1.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── jupyter_events
│   │   │       │   ├── schemas
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _version.py
│   │   │       │   ├── cli.py
│   │   │       │   ├── logger.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── pytest_plugin.py
│   │   │       │   ├── schema_registry.py
│   │   │       │   ├── schema.py
│   │   │       │   ├── traits.py
│   │   │       │   ├── utils.py
│   │   │       │   ├── validators.py
│   │   │       │   └── yaml.py
│   │   │       ├── jupyter_events-0.12.1.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── jupyter_lsp
│   │   │       │   ├── etc
│   │   │       │   ├── schema
│   │   │       │   ├── specs
│   │   │       │   ├── tests
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _version.py
│   │   │       │   ├── constants.py
│   │   │       │   ├── handlers.py
│   │   │       │   ├── manager.py
│   │   │       │   ├── non_blocking.py
│   │   │       │   ├── paths.py
│   │   │       │   ├── serverextension.py
│   │   │       │   ├── session.py
│   │   │       │   ├── stdio.py
│   │   │       │   ├── trait_types.py
│   │   │       │   ├── types.py
│   │   │       │   └── virtual_documents_shadow.py
│   │   │       ├── jupyter_lsp-2.3.1.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── jupyter_server
│   │   │       │   ├── auth
│   │   │       │   ├── base
│   │   │       │   ├── event_schemas
│   │   │       │   ├── extension
│   │   │       │   ├── files
│   │   │       │   ├── gateway
│   │   │       │   ├── i18n
│   │   │       │   ├── kernelspecs
│   │   │       │   ├── nbconvert
│   │   │       │   ├── prometheus
│   │   │       │   ├── services
│   │   │       │   ├── static
│   │   │       │   ├── templates
│   │   │       │   ├── terminal
│   │   │       │   ├── view
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __main__.py
│   │   │       │   ├── _sysinfo.py
│   │   │       │   ├── _tz.py
│   │   │       │   ├── _version.py
│   │   │       │   ├── config_manager.py
│   │   │       │   ├── log.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── pytest_plugin.py
│   │   │       │   ├── serverapp.py
│   │   │       │   ├── traittypes.py
│   │   │       │   ├── transutils.py
│   │   │       │   └── utils.py
│   │   │       ├── jupyter_server_terminals
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _version.py
│   │   │       │   ├── api_handlers.py
│   │   │       │   ├── app.py
│   │   │       │   ├── base.py
│   │   │       │   ├── handlers.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── rest-api.yml
│   │   │       │   └── terminalmanager.py
│   │   │       ├── jupyter_server_terminals-0.5.4.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── jupyter_server-2.20.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── jupyter-1.1.1.dist-info
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── REQUESTED
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── jupyterlab
│   │   │       │   ├── extensions
│   │   │       │   ├── galata
│   │   │       │   ├── handlers
│   │   │       │   ├── schemas
│   │   │       │   ├── staging
│   │   │       │   ├── static
│   │   │       │   ├── tests
│   │   │       │   ├── themes
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __main__.py
│   │   │       │   ├── _version.py
│   │   │       │   ├── browser_check.py
│   │   │       │   ├── browser-test.js
│   │   │       │   ├── commands.py
│   │   │       │   ├── coreconfig.py
│   │   │       │   ├── debuglog.py
│   │   │       │   ├── federated_labextensions.py
│   │   │       │   ├── labapp.py
│   │   │       │   ├── labextensions.py
│   │   │       │   ├── labhubapp.py
│   │   │       │   ├── node-version-check.js
│   │   │       │   ├── pytest_plugin.py
│   │   │       │   ├── serverextension.py
│   │   │       │   ├── style.js
│   │   │       │   ├── upgrade_extension.py
│   │   │       │   └── utils.py
│   │   │       ├── jupyterlab_pygments
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _version.py
│   │   │       │   └── style.py
│   │   │       ├── jupyterlab_pygments-0.3.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── jupyterlab_server
│   │   │       │   ├── templates
│   │   │       │   ├── test_data
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __main__.py
│   │   │       │   ├── _version.py
│   │   │       │   ├── app.py
│   │   │       │   ├── config.py
│   │   │       │   ├── handlers.py
│   │   │       │   ├── licenses_app.py
│   │   │       │   ├── licenses_handler.py
│   │   │       │   ├── listings_handler.py
│   │   │       │   ├── process_app.py
│   │   │       │   ├── process.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── pytest_plugin.py
│   │   │       │   ├── rest-api.yml
│   │   │       │   ├── server.py
│   │   │       │   ├── settings_handler.py
│   │   │       │   ├── settings_utils.py
│   │   │       │   ├── spec.py
│   │   │       │   ├── test_utils.py
│   │   │       │   ├── themes_handler.py
│   │   │       │   ├── translation_utils.py
│   │   │       │   ├── translations_handler.py
│   │   │       │   ├── workspaces_app.py
│   │   │       │   └── workspaces_handler.py
│   │   │       ├── jupyterlab_server-2.28.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── jupyterlab_widgets
│   │   │       │   ├── __init__.py
│   │   │       │   └── _version.py
│   │   │       ├── jupyterlab_widgets-3.0.16.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── jupyterlab-4.6.2.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── kiwisolver
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _cext.cp310-win_amd64.pyd
│   │   │       │   ├── _cext.pyi
│   │   │       │   ├── exceptions.py
│   │   │       │   └── py.typed
│   │   │       ├── kiwisolver-1.5.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── lab
│   │   │       │   ├── calls
│   │   │       │   ├── data
│   │   │       │   ├── reports
│   │   │       │   ├── __init__.py
│   │   │       │   ├── cached_revision.py
│   │   │       │   ├── environments.py
│   │   │       │   ├── experiment.py
│   │   │       │   ├── fetcher.py
│   │   │       │   ├── parser.py
│   │   │       │   ├── steps.py
│   │   │       │   └── tools.py
│   │   │       ├── lab-8.10.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── REQUESTED
│   │   │       │   └── WHEEL
│   │   │       ├── lark
│   │   │       │   ├── __pyinstaller
│   │   │       │   ├── grammars
│   │   │       │   ├── parsers
│   │   │       │   ├── tools
│   │   │       │   ├── __init__.py
│   │   │       │   ├── ast_utils.py
│   │   │       │   ├── common.py
│   │   │       │   ├── exceptions.py
│   │   │       │   ├── grammar.py
│   │   │       │   ├── indenter.py
│   │   │       │   ├── lark.py
│   │   │       │   ├── lexer.py
│   │   │       │   ├── load_grammar.py
│   │   │       │   ├── parse_tree_builder.py
│   │   │       │   ├── parser_frontends.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── reconstruct.py
│   │   │       │   ├── tree_matcher.py
│   │   │       │   ├── tree_templates.py
│   │   │       │   ├── tree.py
│   │   │       │   ├── utils.py
│   │   │       │   └── visitors.py
│   │   │       ├── lark-1.3.1.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── markdown_it
│   │   │       │   ├── cli
│   │   │       │   ├── common
│   │   │       │   ├── helpers
│   │   │       │   ├── presets
│   │   │       │   ├── rules_block
│   │   │       │   ├── rules_core
│   │   │       │   ├── rules_inline
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _compat.py
│   │   │       │   ├── _punycode.py
│   │   │       │   ├── main.py
│   │   │       │   ├── parser_block.py
│   │   │       │   ├── parser_core.py
│   │   │       │   ├── parser_inline.py
│   │   │       │   ├── port.yaml
│   │   │       │   ├── py.typed
│   │   │       │   ├── renderer.py
│   │   │       │   ├── ruler.py
│   │   │       │   ├── token.py
│   │   │       │   ├── tree.py
│   │   │       │   └── utils.py
│   │   │       ├── markdown_it_py-4.2.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── markupsafe
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _native.py
│   │   │       │   ├── _speedups.c
│   │   │       │   ├── _speedups.cp310-win_amd64.pyd
│   │   │       │   ├── _speedups.pyi
│   │   │       │   └── py.typed
│   │   │       ├── markupsafe-3.0.3.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── matplotlib
│   │   │       │   ├── _api
│   │   │       │   ├── axes
│   │   │       │   ├── backends
│   │   │       │   ├── mpl-data
│   │   │       │   ├── projections
│   │   │       │   ├── sphinxext
│   │   │       │   ├── style
│   │   │       │   ├── testing
│   │   │       │   ├── tests
│   │   │       │   ├── tri
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __init__.pyi
│   │   │       │   ├── _afm.py
│   │   │       │   ├── _animation_data.py
│   │   │       │   ├── _blocking_input.py
│   │   │       │   ├── _c_internal_utils.cp310-win_amd64.pyd
│   │   │       │   ├── _c_internal_utils.pyi
│   │   │       │   ├── _cm_bivar.py
│   │   │       │   ├── _cm_listed.py
│   │   │       │   ├── _cm_multivar.py
│   │   │       │   ├── _cm.py
│   │   │       │   ├── _color_data.py
│   │   │       │   ├── _color_data.pyi
│   │   │       │   ├── _constrained_layout.py
│   │   │       │   ├── _docstring.py
│   │   │       │   ├── _docstring.pyi
│   │   │       │   ├── _enums.py
│   │   │       │   ├── _enums.pyi
│   │   │       │   ├── _fontconfig_pattern.py
│   │   │       │   ├── _image.cp310-win_amd64.pyd
│   │   │       │   ├── _image.pyi
│   │   │       │   ├── _internal_utils.py
│   │   │       │   ├── _layoutgrid.py
│   │   │       │   ├── _mathtext_data.py
│   │   │       │   ├── _mathtext.py
│   │   │       │   ├── _path.cp310-win_amd64.pyd
│   │   │       │   ├── _path.pyi
│   │   │       │   ├── _pylab_helpers.py
│   │   │       │   ├── _pylab_helpers.pyi
│   │   │       │   ├── _qhull.cp310-win_amd64.pyd
│   │   │       │   ├── _qhull.pyi
│   │   │       │   ├── _text_helpers.py
│   │   │       │   ├── _tight_bbox.py
│   │   │       │   ├── _tight_layout.py
│   │   │       │   ├── _tri.cp310-win_amd64.pyd
│   │   │       │   ├── _tri.pyi
│   │   │       │   ├── _type1font.py
│   │   │       │   ├── _version.py
│   │   │       │   ├── animation.py
│   │   │       │   ├── animation.pyi
│   │   │       │   ├── artist.py
│   │   │       │   ├── artist.pyi
│   │   │       │   ├── axis.py
│   │   │       │   ├── axis.pyi
│   │   │       │   ├── backend_bases.py
│   │   │       │   ├── backend_bases.pyi
│   │   │       │   ├── backend_managers.py
│   │   │       │   ├── backend_managers.pyi
│   │   │       │   ├── backend_tools.py
│   │   │       │   ├── backend_tools.pyi
│   │   │       │   ├── bezier.py
│   │   │       │   ├── bezier.pyi
│   │   │       │   ├── category.py
│   │   │       │   ├── cbook.py
│   │   │       │   ├── cbook.pyi
│   │   │       │   ├── cm.py
│   │   │       │   ├── cm.pyi
│   │   │       │   ├── collections.py
│   │   │       │   ├── collections.pyi
│   │   │       │   ├── colorbar.py
│   │   │       │   ├── colorbar.pyi
│   │   │       │   ├── colorizer.py
│   │   │       │   ├── colorizer.pyi
│   │   │       │   ├── colors.py
│   │   │       │   ├── colors.pyi
│   │   │       │   ├── container.py
│   │   │       │   ├── container.pyi
│   │   │       │   ├── contour.py
│   │   │       │   ├── contour.pyi
│   │   │       │   ├── dates.py
│   │   │       │   ├── dviread.py
│   │   │       │   ├── dviread.pyi
│   │   │       │   ├── figure.py
│   │   │       │   ├── figure.pyi
│   │   │       │   ├── font_manager.py
│   │   │       │   ├── font_manager.pyi
│   │   │       │   ├── ft2font.cp310-win_amd64.pyd
│   │   │       │   ├── ft2font.pyi
│   │   │       │   ├── gridspec.py
│   │   │       │   ├── gridspec.pyi
│   │   │       │   ├── hatch.py
│   │   │       │   ├── hatch.pyi
│   │   │       │   ├── image.py
│   │   │       │   ├── image.pyi
│   │   │       │   ├── inset.py
│   │   │       │   ├── inset.pyi
│   │   │       │   ├── layout_engine.py
│   │   │       │   ├── layout_engine.pyi
│   │   │       │   ├── legend_handler.py
│   │   │       │   ├── legend_handler.pyi
│   │   │       │   ├── legend.py
│   │   │       │   ├── legend.pyi
│   │   │       │   ├── lines.py
│   │   │       │   ├── lines.pyi
│   │   │       │   ├── markers.py
│   │   │       │   ├── markers.pyi
│   │   │       │   ├── mathtext.py
│   │   │       │   ├── mathtext.pyi
│   │   │       │   ├── mlab.py
│   │   │       │   ├── mlab.pyi
│   │   │       │   ├── offsetbox.py
│   │   │       │   ├── offsetbox.pyi
│   │   │       │   ├── patches.py
│   │   │       │   ├── patches.pyi
│   │   │       │   ├── path.py
│   │   │       │   ├── path.pyi
│   │   │       │   ├── patheffects.py
│   │   │       │   ├── patheffects.pyi
│   │   │       │   ├── py.typed
│   │   │       │   ├── pylab.py
│   │   │       │   ├── pyplot.py
│   │   │       │   ├── quiver.py
│   │   │       │   ├── quiver.pyi
│   │   │       │   ├── rcsetup.py
│   │   │       │   ├── rcsetup.pyi
│   │   │       │   ├── sankey.py
│   │   │       │   ├── sankey.pyi
│   │   │       │   ├── scale.py
│   │   │       │   ├── scale.pyi
│   │   │       │   ├── spines.py
│   │   │       │   ├── spines.pyi
│   │   │       │   ├── stackplot.py
│   │   │       │   ├── stackplot.pyi
│   │   │       │   ├── streamplot.py
│   │   │       │   ├── streamplot.pyi
│   │   │       │   ├── table.py
│   │   │       │   ├── table.pyi
│   │   │       │   ├── texmanager.py
│   │   │       │   ├── texmanager.pyi
│   │   │       │   ├── text.py
│   │   │       │   ├── text.pyi
│   │   │       │   ├── textpath.py
│   │   │       │   ├── textpath.pyi
│   │   │       │   ├── ticker.py
│   │   │       │   ├── ticker.pyi
│   │   │       │   ├── transforms.py
│   │   │       │   ├── transforms.pyi
│   │   │       │   ├── typing.py
│   │   │       │   ├── units.py
│   │   │       │   ├── widgets.py
│   │   │       │   └── widgets.pyi
│   │   │       ├── matplotlib_inline
│   │   │       │   ├── __init__.py
│   │   │       │   ├── backend_inline.py
│   │   │       │   ├── config.py
│   │   │       │   └── py.typed
│   │   │       ├── matplotlib_inline-0.2.2.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── matplotlib-3.10.9.dist-info
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── mdurl
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _decode.py
│   │   │       │   ├── _encode.py
│   │   │       │   ├── _format.py
│   │   │       │   ├── _parse.py
│   │   │       │   ├── _url.py
│   │   │       │   └── py.typed
│   │   │       ├── mdurl-0.1.2.dist-info
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── mistral_common
│   │   │       │   ├── data
│   │   │       │   ├── experimental
│   │   │       │   ├── guidance
│   │   │       │   ├── integrations
│   │   │       │   ├── protocol
│   │   │       │   ├── tokens
│   │   │       │   ├── __init__.py
│   │   │       │   ├── audio.py
│   │   │       │   ├── base.py
│   │   │       │   ├── deprecation.py
│   │   │       │   ├── exceptions.py
│   │   │       │   ├── image.py
│   │   │       │   ├── imports.py
│   │   │       │   ├── multimodal.py
│   │   │       │   └── py.typed
│   │   │       ├── mistral_common-1.11.7.dist-info
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── REQUESTED
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── mistune
│   │   │       │   ├── _inline
│   │   │       │   ├── directives
│   │   │       │   ├── plugins
│   │   │       │   ├── renderers
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __main__.py
│   │   │       │   ├── block_parser.py
│   │   │       │   ├── core.py
│   │   │       │   ├── helpers.py
│   │   │       │   ├── inline_parser.py
│   │   │       │   ├── list_parser.py
│   │   │       │   ├── markdown.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── toc.py
│   │   │       │   └── util.py
│   │   │       ├── mistune-3.3.4.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── mpl_toolkits
│   │   │       │   ├── axes_grid1
│   │   │       │   ├── axisartist
│   │   │       │   └── mplot3d
│   │   │       ├── mpmath
│   │   │       │   ├── calculus
│   │   │       │   ├── functions
│   │   │       │   ├── libmp
│   │   │       │   ├── matrices
│   │   │       │   ├── tests
│   │   │       │   ├── __init__.py
│   │   │       │   ├── ctx_base.py
│   │   │       │   ├── ctx_fp.py
│   │   │       │   ├── ctx_iv.py
│   │   │       │   ├── ctx_mp_python.py
│   │   │       │   ├── ctx_mp.py
│   │   │       │   ├── function_docs.py
│   │   │       │   ├── identification.py
│   │   │       │   ├── math2.py
│   │   │       │   ├── rational.py
│   │   │       │   ├── usertools.py
│   │   │       │   └── visualization.py
│   │   │       ├── mpmath-1.3.0.dist-info
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── msgspec
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __init__.pyi
│   │   │       │   ├── _core.cp310-win_amd64.pyd
│   │   │       │   ├── _json_schema.py
│   │   │       │   ├── _typing_utils.py
│   │   │       │   ├── _typing_utils.pyi
│   │   │       │   ├── _utils.py
│   │   │       │   ├── _version.py
│   │   │       │   ├── inspect.py
│   │   │       │   ├── json.py
│   │   │       │   ├── json.pyi
│   │   │       │   ├── msgpack.py
│   │   │       │   ├── msgpack.pyi
│   │   │       │   ├── py.typed
│   │   │       │   ├── structs.py
│   │   │       │   ├── structs.pyi
│   │   │       │   ├── toml.py
│   │   │       │   └── yaml.py
│   │   │       ├── msgspec-0.21.1.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── multidict
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _abc.py
│   │   │       │   ├── _compat.py
│   │   │       │   ├── _multidict_py.py
│   │   │       │   ├── _multidict.cp310-win_amd64.pyd
│   │   │       │   └── py.typed
│   │   │       ├── multidict-6.7.1.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── multiprocess
│   │   │       │   ├── dummy
│   │   │       │   ├── tests
│   │   │       │   ├── __info__.py
│   │   │       │   ├── __init__.py
│   │   │       │   ├── connection.py
│   │   │       │   ├── context.py
│   │   │       │   ├── forkserver.py
│   │   │       │   ├── heap.py
│   │   │       │   ├── managers.py
│   │   │       │   ├── pool.py
│   │   │       │   ├── popen_fork.py
│   │   │       │   ├── popen_forkserver.py
│   │   │       │   ├── popen_spawn_posix.py
│   │   │       │   ├── popen_spawn_win32.py
│   │   │       │   ├── process.py
│   │   │       │   ├── queues.py
│   │   │       │   ├── reduction.py
│   │   │       │   ├── resource_sharer.py
│   │   │       │   ├── resource_tracker.py
│   │   │       │   ├── shared_memory.py
│   │   │       │   ├── sharedctypes.py
│   │   │       │   ├── spawn.py
│   │   │       │   ├── synchronize.py
│   │   │       │   └── util.py
│   │   │       ├── multiprocess-0.70.16.dist-info
│   │   │       │   ├── COPYING
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── nbclient
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _version.py
│   │   │       │   ├── cli.py
│   │   │       │   ├── client.py
│   │   │       │   ├── exceptions.py
│   │   │       │   ├── jsonutil.py
│   │   │       │   ├── output_widget.py
│   │   │       │   ├── py.typed
│   │   │       │   └── util.py
│   │   │       ├── nbclient-0.11.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── nbconvert
│   │   │       │   ├── exporters
│   │   │       │   ├── filters
│   │   │       │   ├── postprocessors
│   │   │       │   ├── preprocessors
│   │   │       │   ├── resources
│   │   │       │   ├── templates
│   │   │       │   ├── utils
│   │   │       │   ├── writers
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __main__.py
│   │   │       │   ├── _version.py
│   │   │       │   ├── conftest.py
│   │   │       │   ├── nbconvertapp.py
│   │   │       │   └── py.typed
│   │   │       ├── nbconvert-7.17.1.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── nbformat
│   │   │       │   ├── corpus
│   │   │       │   ├── v1
│   │   │       │   ├── v2
│   │   │       │   ├── v3
│   │   │       │   ├── v4
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _imports.py
│   │   │       │   ├── _struct.py
│   │   │       │   ├── _version.py
│   │   │       │   ├── converter.py
│   │   │       │   ├── current.py
│   │   │       │   ├── json_compat.py
│   │   │       │   ├── notebooknode.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── reader.py
│   │   │       │   ├── sentinel.py
│   │   │       │   ├── sign.py
│   │   │       │   ├── validator.py
│   │   │       │   └── warnings.py
│   │   │       ├── nbformat-5.10.4.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── nest_asyncio-1.6.0.dist-info
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── nest_asyncio2-1.7.2.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── networkx
│   │   │       │   ├── algorithms
│   │   │       │   ├── classes
│   │   │       │   ├── drawing
│   │   │       │   ├── generators
│   │   │       │   ├── linalg
│   │   │       │   ├── readwrite
│   │   │       │   ├── tests
│   │   │       │   ├── utils
│   │   │       │   ├── __init__.py
│   │   │       │   ├── conftest.py
│   │   │       │   ├── convert_matrix.py
│   │   │       │   ├── convert.py
│   │   │       │   ├── exception.py
│   │   │       │   ├── lazy_imports.py
│   │   │       │   └── relabel.py
│   │   │       ├── networkx-3.4.2.dist-info
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE.txt
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── notebook
│   │   │       │   ├── custom
│   │   │       │   ├── static
│   │   │       │   ├── templates
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __main__.py
│   │   │       │   ├── _version.py
│   │   │       │   ├── app.py
│   │   │       │   └── py.typed
│   │   │       ├── notebook_shim
│   │   │       │   ├── tests
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _version.py
│   │   │       │   ├── nbserver.py
│   │   │       │   ├── shim.py
│   │   │       │   └── traits.py
│   │   │       ├── notebook_shim-0.2.4.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── notebook-7.6.1.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── numpy
│   │   │       │   ├── _core
│   │   │       │   ├── _pyinstaller
│   │   │       │   ├── _typing
│   │   │       │   ├── _utils
│   │   │       │   ├── char
│   │   │       │   ├── compat
│   │   │       │   ├── core
│   │   │       │   ├── distutils
│   │   │       │   ├── doc
│   │   │       │   ├── f2py
│   │   │       │   ├── fft
│   │   │       │   ├── lib
│   │   │       │   ├── linalg
│   │   │       │   ├── ma
│   │   │       │   ├── matrixlib
│   │   │       │   ├── polynomial
│   │   │       │   ├── random
│   │   │       │   ├── rec
│   │   │       │   ├── strings
│   │   │       │   ├── testing
│   │   │       │   ├── tests
│   │   │       │   ├── typing
│   │   │       │   ├── __config__.py
│   │   │       │   ├── __config__.pyi
│   │   │       │   ├── __init__.cython-30.pxd
│   │   │       │   ├── __init__.pxd
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __init__.pyi
│   │   │       │   ├── _array_api_info.py
│   │   │       │   ├── _array_api_info.pyi
│   │   │       │   ├── _configtool.py
│   │   │       │   ├── _configtool.pyi
│   │   │       │   ├── _distributor_init.py
│   │   │       │   ├── _distributor_init.pyi
│   │   │       │   ├── _expired_attrs_2_0.py
│   │   │       │   ├── _expired_attrs_2_0.pyi
│   │   │       │   ├── _globals.py
│   │   │       │   ├── _globals.pyi
│   │   │       │   ├── _pytesttester.py
│   │   │       │   ├── _pytesttester.pyi
│   │   │       │   ├── conftest.py
│   │   │       │   ├── ctypeslib.py
│   │   │       │   ├── ctypeslib.pyi
│   │   │       │   ├── dtypes.py
│   │   │       │   ├── dtypes.pyi
│   │   │       │   ├── exceptions.py
│   │   │       │   ├── exceptions.pyi
│   │   │       │   ├── matlib.py
│   │   │       │   ├── matlib.pyi
│   │   │       │   ├── py.typed
│   │   │       │   ├── version.py
│   │   │       │   └── version.pyi
│   │   │       ├── numpy-2.2.6.dist-info
│   │   │       │   ├── DELVEWHEEL
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE.txt
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── numpy.libs
│   │   │       │   ├── libscipy_openblas64_-13e2df515630b4a41f92893938845698.dll
│   │   │       │   └── msvcp140-263139962577ecda4cd9469ca360a746.dll
│   │   │       ├── openpyxl
│   │   │       │   ├── cell
│   │   │       │   ├── chart
│   │   │       │   ├── chartsheet
│   │   │       │   ├── comments
│   │   │       │   ├── compat
│   │   │       │   ├── descriptors
│   │   │       │   ├── drawing
│   │   │       │   ├── formatting
│   │   │       │   ├── formula
│   │   │       │   ├── packaging
│   │   │       │   ├── pivot
│   │   │       │   ├── reader
│   │   │       │   ├── styles
│   │   │       │   ├── utils
│   │   │       │   ├── workbook
│   │   │       │   ├── worksheet
│   │   │       │   ├── writer
│   │   │       │   ├── xml
│   │   │       │   ├── __init__.py
│   │   │       │   └── _constants.py
│   │   │       ├── openpyxl-3.1.5.dist-info
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENCE.rst
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── REQUESTED
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── overrides
│   │   │       │   ├── __init__.py
│   │   │       │   ├── enforce.py
│   │   │       │   ├── final.py
│   │   │       │   ├── overrides.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── signature.py
│   │   │       │   └── typing_utils.py
│   │   │       ├── overrides-7.7.0.dist-info
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── packaging
│   │   │       │   ├── licenses
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _elffile.py
│   │   │       │   ├── _manylinux.py
│   │   │       │   ├── _musllinux.py
│   │   │       │   ├── _parser.py
│   │   │       │   ├── _ranges.py
│   │   │       │   ├── _structures.py
│   │   │       │   ├── _tokenizer.py
│   │   │       │   ├── dependency_groups.py
│   │   │       │   ├── direct_url.py
│   │   │       │   ├── errors.py
│   │   │       │   ├── markers.py
│   │   │       │   ├── metadata.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── pylock.py
│   │   │       │   ├── ranges.py
│   │   │       │   ├── requirements.py
│   │   │       │   ├── specifiers.py
│   │   │       │   ├── tags.py
│   │   │       │   ├── utils.py
│   │   │       │   └── version.py
│   │   │       ├── packaging-26.3.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── pandas
│   │   │       │   ├── _config
│   │   │       │   ├── _libs
│   │   │       │   ├── _testing
│   │   │       │   ├── api
│   │   │       │   ├── arrays
│   │   │       │   ├── compat
│   │   │       │   ├── core
│   │   │       │   ├── errors
│   │   │       │   ├── io
│   │   │       │   ├── plotting
│   │   │       │   ├── tests
│   │   │       │   ├── tseries
│   │   │       │   ├── util
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _typing.py
│   │   │       │   ├── _version_meson.py
│   │   │       │   ├── _version.py
│   │   │       │   ├── conftest.py
│   │   │       │   ├── pyproject.toml
│   │   │       │   └── testing.py
│   │   │       ├── pandas-2.3.3.dist-info
│   │   │       │   ├── DELVEWHEEL
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── pandas.libs
│   │   │       │   └── msvcp140-a4c2229bdc2a2a630acdc095b4d86008.dll
│   │   │       ├── pandocfilters-1.5.1.dist-info
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── parso
│   │   │       │   ├── pgen2
│   │   │       │   ├── python
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _compatibility.py
│   │   │       │   ├── cache.py
│   │   │       │   ├── file_io.py
│   │   │       │   ├── grammar.py
│   │   │       │   ├── normalizer.py
│   │   │       │   ├── parser.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── tree.py
│   │   │       │   └── utils.py
│   │   │       ├── parso-0.8.7.dist-info
│   │   │       │   ├── AUTHORS.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE.txt
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── peft
│   │   │       │   ├── optimizers
│   │   │       │   ├── tuners
│   │   │       │   ├── utils
│   │   │       │   ├── __init__.py
│   │   │       │   ├── auto.py
│   │   │       │   ├── config.py
│   │   │       │   ├── functional.py
│   │   │       │   ├── helpers.py
│   │   │       │   ├── import_utils.py
│   │   │       │   ├── mapping_func.py
│   │   │       │   ├── mapping.py
│   │   │       │   ├── mixed_model.py
│   │   │       │   ├── peft_model.py
│   │   │       │   └── py.typed
│   │   │       ├── peft-0.20.0.dist-info
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── REQUESTED
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── PIL
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __main__.py
│   │   │       │   ├── _avif.cp310-win_amd64.pyd
│   │   │       │   ├── _avif.pyi
│   │   │       │   ├── _binary.py
│   │   │       │   ├── _deprecate.py
│   │   │       │   ├── _imaging.cp310-win_amd64.pyd
│   │   │       │   ├── _imaging.pyi
│   │   │       │   ├── _imagingcms.cp310-win_amd64.pyd
│   │   │       │   ├── _imagingcms.pyi
│   │   │       │   ├── _imagingft.cp310-win_amd64.pyd
│   │   │       │   ├── _imagingft.pyi
│   │   │       │   ├── _imagingmath.cp310-win_amd64.pyd
│   │   │       │   ├── _imagingmath.pyi
│   │   │       │   ├── _imagingmorph.cp310-win_amd64.pyd
│   │   │       │   ├── _imagingmorph.pyi
│   │   │       │   ├── _imagingtk.cp310-win_amd64.pyd
│   │   │       │   ├── _imagingtk.pyi
│   │   │       │   ├── _tkinter_finder.py
│   │   │       │   ├── _typing.py
│   │   │       │   ├── _util.py
│   │   │       │   ├── _version.py
│   │   │       │   ├── _webp.cp310-win_amd64.pyd
│   │   │       │   ├── _webp.pyi
│   │   │       │   ├── AvifImagePlugin.py
│   │   │       │   ├── BdfFontFile.py
│   │   │       │   ├── BlpImagePlugin.py
│   │   │       │   ├── BmpImagePlugin.py
│   │   │       │   ├── BufrStubImagePlugin.py
│   │   │       │   ├── ContainerIO.py
│   │   │       │   ├── CurImagePlugin.py
│   │   │       │   ├── DcxImagePlugin.py
│   │   │       │   ├── DdsImagePlugin.py
│   │   │       │   ├── EpsImagePlugin.py
│   │   │       │   ├── ExifTags.py
│   │   │       │   ├── features.py
│   │   │       │   ├── FitsImagePlugin.py
│   │   │       │   ├── FliImagePlugin.py
│   │   │       │   ├── FontFile.py
│   │   │       │   ├── FpxImagePlugin.py
│   │   │       │   ├── FtexImagePlugin.py
│   │   │       │   ├── GbrImagePlugin.py
│   │   │       │   ├── GdImageFile.py
│   │   │       │   ├── GifImagePlugin.py
│   │   │       │   ├── GimpGradientFile.py
│   │   │       │   ├── GimpPaletteFile.py
│   │   │       │   ├── GribStubImagePlugin.py
│   │   │       │   ├── Hdf5StubImagePlugin.py
│   │   │       │   ├── IcnsImagePlugin.py
│   │   │       │   ├── IcoImagePlugin.py
│   │   │       │   ├── Image.py
│   │   │       │   ├── ImageChops.py
│   │   │       │   ├── ImageCms.py
│   │   │       │   ├── ImageColor.py
│   │   │       │   ├── ImageDraw.py
│   │   │       │   ├── ImageDraw2.py
│   │   │       │   ├── ImageEnhance.py
│   │   │       │   ├── ImageFile.py
│   │   │       │   ├── ImageFilter.py
│   │   │       │   ├── ImageFont.py
│   │   │       │   ├── ImageGrab.py
│   │   │       │   ├── ImageMath.py
│   │   │       │   ├── ImageMode.py
│   │   │       │   ├── ImageMorph.py
│   │   │       │   ├── ImageOps.py
│   │   │       │   ├── ImagePalette.py
│   │   │       │   ├── ImagePath.py
│   │   │       │   ├── ImageQt.py
│   │   │       │   ├── ImageSequence.py
│   │   │       │   ├── ImageShow.py
│   │   │       │   ├── ImageStat.py
│   │   │       │   ├── ImageText.py
│   │   │       │   ├── ImageTk.py
│   │   │       │   ├── ImageTransform.py
│   │   │       │   ├── ImageWin.py
│   │   │       │   ├── ImImagePlugin.py
│   │   │       │   ├── ImtImagePlugin.py
│   │   │       │   ├── IptcImagePlugin.py
│   │   │       │   ├── Jpeg2KImagePlugin.py
│   │   │       │   ├── JpegImagePlugin.py
│   │   │       │   ├── JpegPresets.py
│   │   │       │   ├── McIdasImagePlugin.py
│   │   │       │   ├── MicImagePlugin.py
│   │   │       │   ├── MpegImagePlugin.py
│   │   │       │   ├── MpoImagePlugin.py
│   │   │       │   ├── MspImagePlugin.py
│   │   │       │   ├── PaletteFile.py
│   │   │       │   ├── PalmImagePlugin.py
│   │   │       │   ├── PcdImagePlugin.py
│   │   │       │   ├── PcfFontFile.py
│   │   │       │   ├── PcxImagePlugin.py
│   │   │       │   ├── PdfImagePlugin.py
│   │   │       │   ├── PdfParser.py
│   │   │       │   ├── PixarImagePlugin.py
│   │   │       │   ├── PngImagePlugin.py
│   │   │       │   ├── PpmImagePlugin.py
│   │   │       │   ├── PsdImagePlugin.py
│   │   │       │   ├── PSDraw.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── QoiImagePlugin.py
│   │   │       │   ├── report.py
│   │   │       │   ├── SgiImagePlugin.py
│   │   │       │   ├── SpiderImagePlugin.py
│   │   │       │   ├── SunImagePlugin.py
│   │   │       │   ├── TarIO.py
│   │   │       │   ├── TgaImagePlugin.py
│   │   │       │   ├── TiffImagePlugin.py
│   │   │       │   ├── TiffTags.py
│   │   │       │   ├── WalImageFile.py
│   │   │       │   ├── WebPImagePlugin.py
│   │   │       │   ├── WmfImagePlugin.py
│   │   │       │   ├── XbmImagePlugin.py
│   │   │       │   ├── XpmImagePlugin.py
│   │   │       │   └── XVThumbImagePlugin.py
│   │   │       ├── pillow-12.2.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   ├── WHEEL
│   │   │       │   └── zip-safe
│   │   │       ├── pip
│   │   │       │   ├── _internal
│   │   │       │   ├── _vendor
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __main__.py
│   │   │       │   ├── __pip-runner__.py
│   │   │       │   └── py.typed
│   │   │       ├── pip-26.2.1.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── REQUESTED
│   │   │       │   └── WHEEL
│   │   │       ├── pkg_resources
│   │   │       │   ├── tests
│   │   │       │   ├── __init__.py
│   │   │       │   ├── api_tests.txt
│   │   │       │   └── py.typed
│   │   │       ├── platformdirs
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __main__.py
│   │   │       │   ├── _xdg.py
│   │   │       │   ├── android.py
│   │   │       │   ├── api.py
│   │   │       │   ├── macos.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── unix.py
│   │   │       │   ├── version.py
│   │   │       │   └── windows.py
│   │   │       ├── platformdirs-4.11.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── prometheus_client
│   │   │       │   ├── aiohttp
│   │   │       │   ├── bridge
│   │   │       │   ├── django
│   │   │       │   ├── openmetrics
│   │   │       │   ├── twisted
│   │   │       │   ├── __init__.py
│   │   │       │   ├── asgi.py
│   │   │       │   ├── context_managers.py
│   │   │       │   ├── core.py
│   │   │       │   ├── decorator.py
│   │   │       │   ├── exposition.py
│   │   │       │   ├── gc_collector.py
│   │   │       │   ├── metrics_core.py
│   │   │       │   ├── metrics.py
│   │   │       │   ├── mmap_dict.py
│   │   │       │   ├── multiprocess.py
│   │   │       │   ├── parser.py
│   │   │       │   ├── platform_collector.py
│   │   │       │   ├── process_collector.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── registry.py
│   │   │       │   ├── samples.py
│   │   │       │   ├── utils.py
│   │   │       │   ├── validation.py
│   │   │       │   └── values.py
│   │   │       ├── prometheus_client-0.26.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── prompt_toolkit
│   │   │       │   ├── application
│   │   │       │   ├── clipboard
│   │   │       │   ├── completion
│   │   │       │   ├── contrib
│   │   │       │   ├── eventloop
│   │   │       │   ├── filters
│   │   │       │   ├── formatted_text
│   │   │       │   ├── input
│   │   │       │   ├── key_binding
│   │   │       │   ├── layout
│   │   │       │   ├── lexers
│   │   │       │   ├── output
│   │   │       │   ├── shortcuts
│   │   │       │   ├── styles
│   │   │       │   ├── widgets
│   │   │       │   ├── __init__.py
│   │   │       │   ├── auto_suggest.py
│   │   │       │   ├── buffer.py
│   │   │       │   ├── cache.py
│   │   │       │   ├── cursor_shapes.py
│   │   │       │   ├── data_structures.py
│   │   │       │   ├── document.py
│   │   │       │   ├── enums.py
│   │   │       │   ├── history.py
│   │   │       │   ├── keys.py
│   │   │       │   ├── log.py
│   │   │       │   ├── mouse_events.py
│   │   │       │   ├── patch_stdout.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── renderer.py
│   │   │       │   ├── search.py
│   │   │       │   ├── selection.py
│   │   │       │   ├── token.py
│   │   │       │   ├── utils.py
│   │   │       │   ├── validation.py
│   │   │       │   └── win32_types.py
│   │   │       ├── prompt_toolkit-3.0.53.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── propcache
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _helpers_c.cp310-win_amd64.pyd
│   │   │       │   ├── _helpers_c.pyx
│   │   │       │   ├── _helpers_py.py
│   │   │       │   ├── _helpers.py
│   │   │       │   ├── api.py
│   │   │       │   └── py.typed
│   │   │       ├── propcache-0.5.2.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── protobuf-7.35.1.dist-info
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── psutil
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _common.py
│   │   │       │   ├── _ntuples.py
│   │   │       │   ├── _psaix.py
│   │   │       │   ├── _psbsd.py
│   │   │       │   ├── _pslinux.py
│   │   │       │   ├── _psosx.py
│   │   │       │   ├── _psposix.py
│   │   │       │   ├── _pssunos.py
│   │   │       │   ├── _psutil_windows.pyd
│   │   │       │   └── _pswindows.py
│   │   │       ├── psutil-7.2.2.dist-info
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── pure_eval
│   │   │       │   ├── __init__.py
│   │   │       │   ├── core.py
│   │   │       │   ├── my_getattr_static.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── utils.py
│   │   │       │   └── version.py
│   │   │       ├── pure_eval-0.2.3.dist-info
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE.txt
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── pyarrow
│   │   │       │   ├── include
│   │   │       │   ├── includes
│   │   │       │   ├── interchange
│   │   │       │   ├── parquet
│   │   │       │   ├── src
│   │   │       │   ├── tests
│   │   │       │   ├── vendored
│   │   │       │   ├── __init__.pxd
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _acero.cp310-win_amd64.pyd
│   │   │       │   ├── _acero.pxd
│   │   │       │   ├── _acero.pyx
│   │   │       │   ├── _azurefs.cp310-win_amd64.pyd
│   │   │       │   ├── _azurefs.pyx
│   │   │       │   ├── _compute_docstrings.py
│   │   │       │   ├── _compute.cp310-win_amd64.pyd
│   │   │       │   ├── _compute.pxd
│   │   │       │   ├── _compute.pyx
│   │   │       │   ├── _csv.cp310-win_amd64.pyd
│   │   │       │   ├── _csv.pxd
│   │   │       │   ├── _csv.pyx
│   │   │       │   ├── _cuda.pxd
│   │   │       │   ├── _cuda.pyx
│   │   │       │   ├── _dataset_orc.cp310-win_amd64.pyd
│   │   │       │   ├── _dataset_orc.pyx
│   │   │       │   ├── _dataset_parquet_encryption.cp310-win_amd64.pyd
│   │   │       │   ├── _dataset_parquet_encryption.pyx
│   │   │       │   ├── _dataset_parquet.cp310-win_amd64.pyd
│   │   │       │   ├── _dataset_parquet.pxd
│   │   │       │   ├── _dataset_parquet.pyx
│   │   │       │   ├── _dataset.cp310-win_amd64.pyd
│   │   │       │   ├── _dataset.pxd
│   │   │       │   ├── _dataset.pyx
│   │   │       │   ├── _dlpack.pxi
│   │   │       │   ├── _feather.cp310-win_amd64.pyd
│   │   │       │   ├── _feather.pyx
│   │   │       │   ├── _flight.cp310-win_amd64.pyd
│   │   │       │   ├── _flight.pyx
│   │   │       │   ├── _fs.cp310-win_amd64.pyd
│   │   │       │   ├── _fs.pxd
│   │   │       │   ├── _fs.pyx
│   │   │       │   ├── _gcsfs.cp310-win_amd64.pyd
│   │   │       │   ├── _gcsfs.pyx
│   │   │       │   ├── _generated_version.py
│   │   │       │   ├── _hdfs.cp310-win_amd64.pyd
│   │   │       │   ├── _hdfs.pyx
│   │   │       │   ├── _json.cp310-win_amd64.pyd
│   │   │       │   ├── _json.pxd
│   │   │       │   ├── _json.pyx
│   │   │       │   ├── _orc.cp310-win_amd64.pyd
│   │   │       │   ├── _orc.pxd
│   │   │       │   ├── _orc.pyx
│   │   │       │   ├── _parquet_encryption.cp310-win_amd64.pyd
│   │   │       │   ├── _parquet_encryption.pxd
│   │   │       │   ├── _parquet_encryption.pyx
│   │   │       │   ├── _parquet.cp310-win_amd64.pyd
│   │   │       │   ├── _parquet.pxd
│   │   │       │   ├── _parquet.pyx
│   │   │       │   ├── _pyarrow_cpp_tests.cp310-win_amd64.pyd
│   │   │       │   ├── _pyarrow_cpp_tests.pxd
│   │   │       │   ├── _pyarrow_cpp_tests.pyx
│   │   │       │   ├── _s3fs.cp310-win_amd64.pyd
│   │   │       │   ├── _s3fs.pyx
│   │   │       │   ├── _substrait.cp310-win_amd64.pyd
│   │   │       │   ├── _substrait.pyx
│   │   │       │   ├── acero.py
│   │   │       │   ├── array.pxi
│   │   │       │   ├── arrow_acero.dll
│   │   │       │   ├── arrow_acero.lib
│   │   │       │   ├── arrow_compute.dll
│   │   │       │   ├── arrow_compute.lib
│   │   │       │   ├── arrow_dataset.dll
│   │   │       │   ├── arrow_dataset.lib
│   │   │       │   ├── arrow_flight.dll
│   │   │       │   ├── arrow_flight.lib
│   │   │       │   ├── arrow_python_flight.dll
│   │   │       │   ├── arrow_python_flight.lib
│   │   │       │   ├── arrow_python_parquet_encryption.dll
│   │   │       │   ├── arrow_python_parquet_encryption.lib
│   │   │       │   ├── arrow_python.dll
│   │   │       │   ├── arrow_python.lib
│   │   │       │   ├── arrow_substrait.dll
│   │   │       │   ├── arrow_substrait.lib
│   │   │       │   ├── arrow.dll
│   │   │       │   ├── arrow.lib
│   │   │       │   ├── benchmark.pxi
│   │   │       │   ├── benchmark.py
│   │   │       │   ├── builder.pxi
│   │   │       │   ├── cffi.py
│   │   │       │   ├── compat.pxi
│   │   │       │   ├── compute.py
│   │   │       │   ├── config.pxi
│   │   │       │   ├── conftest.py
│   │   │       │   ├── csv.py
│   │   │       │   ├── cuda.py
│   │   │       │   ├── dataset.py
│   │   │       │   ├── device.pxi
│   │   │       │   ├── error.pxi
│   │   │       │   ├── feather.py
│   │   │       │   ├── flight.py
│   │   │       │   ├── fs.py
│   │   │       │   ├── gandiva.pyx
│   │   │       │   ├── io.pxi
│   │   │       │   ├── ipc.pxi
│   │   │       │   ├── ipc.py
│   │   │       │   ├── json.py
│   │   │       │   ├── jvm.py
│   │   │       │   ├── lib.cp310-win_amd64.pyd
│   │   │       │   ├── lib.pxd
│   │   │       │   ├── lib.pyx
│   │   │       │   ├── memory.pxi
│   │   │       │   ├── orc.py
│   │   │       │   ├── pandas_compat.py
│   │   │       │   ├── pandas-shim.pxi
│   │   │       │   ├── parquet.dll
│   │   │       │   ├── parquet.lib
│   │   │       │   ├── public-api.pxi
│   │   │       │   ├── scalar.pxi
│   │   │       │   ├── substrait.py
│   │   │       │   ├── table.pxi
│   │   │       │   ├── tensor.pxi
│   │   │       │   ├── types.pxi
│   │   │       │   ├── types.py
│   │   │       │   └── util.py
│   │   │       ├── pyarrow-25.0.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── DELVEWHEEL
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── pyarrow.libs
│   │   │       │   ├── msvcp140_atomic_wait-4bec1bd7c3f445519c6c93c879884a89.dll
│   │   │       │   └── msvcp140-d448dcabdad98c14abc6ff2741df95cd.dll
│   │   │       ├── pycountry
│   │   │       │   ├── databases
│   │   │       │   ├── locales
│   │   │       │   ├── tests
│   │   │       │   ├── __init__.py
│   │   │       │   ├── COPYRIGHT.txt
│   │   │       │   ├── db.py
│   │   │       │   └── py.typed
│   │   │       ├── pycountry-26.2.16.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── pycparser
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _ast_gen.py
│   │   │       │   ├── _c_ast.cfg
│   │   │       │   ├── ast_transforms.py
│   │   │       │   ├── c_ast.py
│   │   │       │   ├── c_generator.py
│   │   │       │   ├── c_lexer.py
│   │   │       │   └── c_parser.py
│   │   │       ├── pycparser-3.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── pydantic
│   │   │       │   ├── _internal
│   │   │       │   ├── deprecated
│   │   │       │   ├── experimental
│   │   │       │   ├── plugin
│   │   │       │   ├── v1
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _migration.py
│   │   │       │   ├── alias_generators.py
│   │   │       │   ├── aliases.py
│   │   │       │   ├── annotated_handlers.py
│   │   │       │   ├── class_validators.py
│   │   │       │   ├── color.py
│   │   │       │   ├── config.py
│   │   │       │   ├── dataclasses.py
│   │   │       │   ├── datetime_parse.py
│   │   │       │   ├── decorator.py
│   │   │       │   ├── env_settings.py
│   │   │       │   ├── error_wrappers.py
│   │   │       │   ├── errors.py
│   │   │       │   ├── fields.py
│   │   │       │   ├── functional_serializers.py
│   │   │       │   ├── functional_validators.py
│   │   │       │   ├── generics.py
│   │   │       │   ├── json_schema.py
│   │   │       │   ├── json.py
│   │   │       │   ├── main.py
│   │   │       │   ├── mypy.py
│   │   │       │   ├── networks.py
│   │   │       │   ├── parse.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── root_model.py
│   │   │       │   ├── schema.py
│   │   │       │   ├── tools.py
│   │   │       │   ├── type_adapter.py
│   │   │       │   ├── types.py
│   │   │       │   ├── typing.py
│   │   │       │   ├── utils.py
│   │   │       │   ├── validate_call_decorator.py
│   │   │       │   ├── validators.py
│   │   │       │   ├── version.py
│   │   │       │   └── warnings.py
│   │   │       ├── pydantic_core
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _pydantic_core.cp310-win_amd64.pyd
│   │   │       │   ├── _pydantic_core.pyi
│   │   │       │   ├── core_schema.py
│   │   │       │   └── py.typed
│   │   │       ├── pydantic_core-2.46.4.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── sboms
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── pydantic_extra_types
│   │   │       │   ├── __init__.py
│   │   │       │   ├── color.py
│   │   │       │   ├── coordinate.py
│   │   │       │   ├── country.py
│   │   │       │   ├── cron.py
│   │   │       │   ├── currency_code.py
│   │   │       │   ├── domain.py
│   │   │       │   ├── dsn.py
│   │   │       │   ├── epoch.py
│   │   │       │   ├── iban.py
│   │   │       │   ├── isbn.py
│   │   │       │   ├── language_code.py
│   │   │       │   ├── mac_address.py
│   │   │       │   ├── mime_types.py
│   │   │       │   ├── mongo_object_id.py
│   │   │       │   ├── path.py
│   │   │       │   ├── payment.py
│   │   │       │   ├── pendulum_dt.py
│   │   │       │   ├── phone_numbers.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── routing_number.py
│   │   │       │   ├── s3.py
│   │   │       │   ├── script_code.py
│   │   │       │   ├── semantic_version.py
│   │   │       │   ├── semver.py
│   │   │       │   ├── timezone_name.py
│   │   │       │   ├── ulid.py
│   │   │       │   └── uuid_types.py
│   │   │       ├── pydantic_extra_types-2.11.1.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── pydantic-2.13.4.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── pygments
│   │   │       │   ├── filters
│   │   │       │   ├── formatters
│   │   │       │   ├── lexers
│   │   │       │   ├── styles
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __main__.py
│   │   │       │   ├── cmdline.py
│   │   │       │   ├── console.py
│   │   │       │   ├── filter.py
│   │   │       │   ├── formatter.py
│   │   │       │   ├── lexer.py
│   │   │       │   ├── modeline.py
│   │   │       │   ├── plugin.py
│   │   │       │   ├── regexopt.py
│   │   │       │   ├── scanner.py
│   │   │       │   ├── sphinxext.py
│   │   │       │   ├── style.py
│   │   │       │   ├── token.py
│   │   │       │   ├── unistring.py
│   │   │       │   └── util.py
│   │   │       ├── pygments-2.20.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── pyparsing
│   │   │       │   ├── ai
│   │   │       │   ├── diagram
│   │   │       │   ├── tools
│   │   │       │   ├── __init__.py
│   │   │       │   ├── actions.py
│   │   │       │   ├── common.py
│   │   │       │   ├── core.py
│   │   │       │   ├── exceptions.py
│   │   │       │   ├── helpers.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── results.py
│   │   │       │   ├── testing.py
│   │   │       │   ├── unicode.py
│   │   │       │   ├── util.py
│   │   │       │   └── warnings.py
│   │   │       ├── pyparsing-3.3.2.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── python_dateutil-2.9.0.post0.dist-info
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   ├── WHEEL
│   │   │       │   └── zip-safe
│   │   │       ├── python_json_logger-4.1.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── pythonjsonlogger
│   │   │       │   ├── __init__.py
│   │   │       │   ├── core.py
│   │   │       │   ├── defaults.py
│   │   │       │   ├── exception.py
│   │   │       │   ├── json.py
│   │   │       │   ├── jsonlogger.py
│   │   │       │   ├── msgspec.py
│   │   │       │   ├── orjson.py
│   │   │       │   ├── py.typed
│   │   │       │   └── utils.py
│   │   │       ├── pytz
│   │   │       │   ├── zoneinfo
│   │   │       │   ├── __init__.py
│   │   │       │   ├── exceptions.py
│   │   │       │   ├── lazy.py
│   │   │       │   ├── reference.py
│   │   │       │   ├── tzfile.py
│   │   │       │   └── tzinfo.py
│   │   │       ├── pytz-2026.3.post1.dist-info
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE.txt
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   ├── WHEEL
│   │   │       │   └── zip-safe
│   │   │       ├── pywinpty-3.0.5.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── sboms
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── pyyaml-6.0.3.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── pyzmq-27.1.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── referencing
│   │   │       │   ├── tests
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _attrs.py
│   │   │       │   ├── _attrs.pyi
│   │   │       │   ├── _core.py
│   │   │       │   ├── exceptions.py
│   │   │       │   ├── jsonschema.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── retrieval.py
│   │   │       │   └── typing.py
│   │   │       ├── referencing-0.37.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── regex
│   │   │       │   ├── tests
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _main.py
│   │   │       │   ├── _regex_core.py
│   │   │       │   └── _regex.cp310-win_amd64.pyd
│   │   │       ├── regex-2026.7.19.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── requests
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __version__.py
│   │   │       │   ├── _internal_utils.py
│   │   │       │   ├── _types.py
│   │   │       │   ├── adapters.py
│   │   │       │   ├── api.py
│   │   │       │   ├── auth.py
│   │   │       │   ├── certs.py
│   │   │       │   ├── compat.py
│   │   │       │   ├── cookies.py
│   │   │       │   ├── exceptions.py
│   │   │       │   ├── help.py
│   │   │       │   ├── hooks.py
│   │   │       │   ├── models.py
│   │   │       │   ├── packages.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── sessions.py
│   │   │       │   ├── status_codes.py
│   │   │       │   ├── structures.py
│   │   │       │   └── utils.py
│   │   │       ├── requests-2.34.2.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── rfc3339_validator-0.1.4.dist-info
│   │   │       │   ├── AUTHORS.rst
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── rfc3986_validator-0.1.1.dist-info
│   │   │       │   ├── AUTHORS.rst
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── rfc3987_syntax
│   │   │       │   ├── __init__.py
│   │   │       │   ├── CITATION.cff
│   │   │       │   ├── syntax_helpers.py
│   │   │       │   ├── syntax_rfc3987.lark
│   │   │       │   └── utils.py
│   │   │       ├── rfc3987_syntax-1.1.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── rich
│   │   │       │   ├── _unicode_data
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __main__.py
│   │   │       │   ├── _emoji_codes.py
│   │   │       │   ├── _emoji_replace.py
│   │   │       │   ├── _export_format.py
│   │   │       │   ├── _extension.py
│   │   │       │   ├── _fileno.py
│   │   │       │   ├── _inspect.py
│   │   │       │   ├── _log_render.py
│   │   │       │   ├── _loop.py
│   │   │       │   ├── _null_file.py
│   │   │       │   ├── _palettes.py
│   │   │       │   ├── _pick.py
│   │   │       │   ├── _ratio.py
│   │   │       │   ├── _spinners.py
│   │   │       │   ├── _stack.py
│   │   │       │   ├── _timer.py
│   │   │       │   ├── _win32_console.py
│   │   │       │   ├── _windows_renderer.py
│   │   │       │   ├── _windows.py
│   │   │       │   ├── _wrap.py
│   │   │       │   ├── abc.py
│   │   │       │   ├── align.py
│   │   │       │   ├── ansi.py
│   │   │       │   ├── bar.py
│   │   │       │   ├── box.py
│   │   │       │   ├── cells.py
│   │   │       │   ├── color_triplet.py
│   │   │       │   ├── color.py
│   │   │       │   ├── columns.py
│   │   │       │   ├── console.py
│   │   │       │   ├── constrain.py
│   │   │       │   ├── containers.py
│   │   │       │   ├── control.py
│   │   │       │   ├── default_styles.py
│   │   │       │   ├── diagnose.py
│   │   │       │   ├── emoji.py
│   │   │       │   ├── errors.py
│   │   │       │   ├── file_proxy.py
│   │   │       │   ├── filesize.py
│   │   │       │   ├── highlighter.py
│   │   │       │   ├── json.py
│   │   │       │   ├── jupyter.py
│   │   │       │   ├── layout.py
│   │   │       │   ├── live_render.py
│   │   │       │   ├── live.py
│   │   │       │   ├── logging.py
│   │   │       │   ├── markdown.py
│   │   │       │   ├── markup.py
│   │   │       │   ├── measure.py
│   │   │       │   ├── padding.py
│   │   │       │   ├── pager.py
│   │   │       │   ├── palette.py
│   │   │       │   ├── panel.py
│   │   │       │   ├── pretty.py
│   │   │       │   ├── progress_bar.py
│   │   │       │   ├── progress.py
│   │   │       │   ├── prompt.py
│   │   │       │   ├── protocol.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── region.py
│   │   │       │   ├── repr.py
│   │   │       │   ├── rule.py
│   │   │       │   ├── scope.py
│   │   │       │   ├── screen.py
│   │   │       │   ├── segment.py
│   │   │       │   ├── spinner.py
│   │   │       │   ├── status.py
│   │   │       │   ├── style.py
│   │   │       │   ├── styled.py
│   │   │       │   ├── syntax.py
│   │   │       │   ├── table.py
│   │   │       │   ├── terminal_theme.py
│   │   │       │   ├── text.py
│   │   │       │   ├── theme.py
│   │   │       │   ├── themes.py
│   │   │       │   ├── traceback.py
│   │   │       │   └── tree.py
│   │   │       ├── rich-15.0.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── rpds
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __init__.pyi
│   │   │       │   ├── py.typed
│   │   │       │   └── rpds.cp310-win_amd64.pyd
│   │   │       ├── rpds_py-0.30.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── safetensors
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __init__.pyi
│   │   │       │   ├── _safetensors_rust.pyd
│   │   │       │   ├── flax.py
│   │   │       │   ├── mlx.py
│   │   │       │   ├── numpy.py
│   │   │       │   ├── paddle.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── tensorflow.py
│   │   │       │   └── torch.py
│   │   │       ├── safetensors-0.8.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── sboms
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── scikit_learn-1.7.2.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── REQUESTED
│   │   │       │   └── WHEEL
│   │   │       ├── scipy
│   │   │       │   ├── _lib
│   │   │       │   ├── cluster
│   │   │       │   ├── constants
│   │   │       │   ├── datasets
│   │   │       │   ├── differentiate
│   │   │       │   ├── fft
│   │   │       │   ├── fftpack
│   │   │       │   ├── integrate
│   │   │       │   ├── interpolate
│   │   │       │   ├── io
│   │   │       │   ├── linalg
│   │   │       │   ├── misc
│   │   │       │   ├── ndimage
│   │   │       │   ├── odr
│   │   │       │   ├── optimize
│   │   │       │   ├── signal
│   │   │       │   ├── sparse
│   │   │       │   ├── spatial
│   │   │       │   ├── special
│   │   │       │   ├── stats
│   │   │       │   ├── __config__.py
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _distributor_init.py
│   │   │       │   ├── conftest.py
│   │   │       │   └── version.py
│   │   │       ├── scipy-1.15.3.dist-info
│   │   │       │   ├── DELVEWHEEL
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE.txt
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── scipy.libs
│   │   │       │   └── libscipy_openblas-f07f5a5d207a3a47104dca54d6d0c86a.dll
│   │   │       ├── scripts
│   │   │       │   ├── enforce_kwargs_spacing.py
│   │   │       │   ├── lint_workflow_triggers.py
│   │   │       │   ├── scan_packages.py
│   │   │       │   └── verify_comment_only_diff.py
│   │   │       ├── seaborn
│   │   │       │   ├── _core
│   │   │       │   ├── _marks
│   │   │       │   ├── _stats
│   │   │       │   ├── colors
│   │   │       │   ├── external
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _base.py
│   │   │       │   ├── _compat.py
│   │   │       │   ├── _docstrings.py
│   │   │       │   ├── _statistics.py
│   │   │       │   ├── _testing.py
│   │   │       │   ├── algorithms.py
│   │   │       │   ├── axisgrid.py
│   │   │       │   ├── categorical.py
│   │   │       │   ├── cm.py
│   │   │       │   ├── distributions.py
│   │   │       │   ├── matrix.py
│   │   │       │   ├── miscplot.py
│   │   │       │   ├── objects.py
│   │   │       │   ├── palettes.py
│   │   │       │   ├── rcmod.py
│   │   │       │   ├── regression.py
│   │   │       │   ├── relational.py
│   │   │       │   ├── utils.py
│   │   │       │   └── widgets.py
│   │   │       ├── seaborn-0.13.2.dist-info
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE.md
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── REQUESTED
│   │   │       │   └── WHEEL
│   │   │       ├── send2trash
│   │   │       │   ├── mac
│   │   │       │   ├── win
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __main__.py
│   │   │       │   ├── exceptions.py
│   │   │       │   ├── plat_gio.py
│   │   │       │   ├── plat_other.py
│   │   │       │   └── util.py
│   │   │       ├── send2trash-2.1.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── sentencepiece
│   │   │       │   ├── package_data
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __init__.pyi
│   │   │       │   ├── _sentencepiece.cp310-win_amd64.pyd
│   │   │       │   ├── _version.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── sentencepiece_model_pb2.py
│   │   │       │   ├── sentencepiece_pb2.py
│   │   │       │   └── sentencepiece_pybind.cc
│   │   │       ├── sentencepiece-0.2.2.dist-info
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── setuptools
│   │   │       │   ├── _distutils
│   │   │       │   ├── _vendor
│   │   │       │   ├── command
│   │   │       │   ├── compat
│   │   │       │   ├── config
│   │   │       │   ├── tests
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _core_metadata.py
│   │   │       │   ├── _entry_points.py
│   │   │       │   ├── _imp.py
│   │   │       │   ├── _importlib.py
│   │   │       │   ├── _itertools.py
│   │   │       │   ├── _normalization.py
│   │   │       │   ├── _path.py
│   │   │       │   ├── _reqs.py
│   │   │       │   ├── _shutil.py
│   │   │       │   ├── _static.py
│   │   │       │   ├── archive_util.py
│   │   │       │   ├── build_meta.py
│   │   │       │   ├── cli-32.exe
│   │   │       │   ├── cli-64.exe
│   │   │       │   ├── cli-arm64.exe
│   │   │       │   ├── cli.exe
│   │   │       │   ├── depends.py
│   │   │       │   ├── discovery.py
│   │   │       │   ├── dist.py
│   │   │       │   ├── errors.py
│   │   │       │   ├── extension.py
│   │   │       │   ├── glob.py
│   │   │       │   ├── gui-32.exe
│   │   │       │   ├── gui-64.exe
│   │   │       │   ├── gui-arm64.exe
│   │   │       │   ├── gui.exe
│   │   │       │   ├── installer.py
│   │   │       │   ├── launch.py
│   │   │       │   ├── logging.py
│   │   │       │   ├── modified.py
│   │   │       │   ├── monkey.py
│   │   │       │   ├── msvc.py
│   │   │       │   ├── namespaces.py
│   │   │       │   ├── package_index.py
│   │   │       │   ├── sandbox.py
│   │   │       │   ├── script (dev).tmpl
│   │   │       │   ├── script.tmpl
│   │   │       │   ├── unicode_utils.py
│   │   │       │   ├── version.py
│   │   │       │   ├── warnings.py
│   │   │       │   ├── wheel.py
│   │   │       │   └── windows_support.py
│   │   │       ├── setuptools-78.1.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── shellingham
│   │   │       │   ├── posix
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _core.py
│   │   │       │   └── nt.py
│   │   │       ├── shellingham-1.5.4.dist-info
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   ├── WHEEL
│   │   │       │   └── zip-safe
│   │   │       ├── simplejson
│   │   │       │   ├── tests
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _speedups.cp310-win_amd64.pyd
│   │   │       │   ├── compat.py
│   │   │       │   ├── decoder.py
│   │   │       │   ├── encoder.py
│   │   │       │   ├── errors.py
│   │   │       │   ├── ordered_dict.py
│   │   │       │   ├── raw_json.py
│   │   │       │   ├── scanner.py
│   │   │       │   └── tool.py
│   │   │       ├── simplejson-4.1.1.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── six-1.17.0.dist-info
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── sklearn
│   │   │       │   ├── __check_build
│   │   │       │   ├── _build_utils
│   │   │       │   ├── _loss
│   │   │       │   ├── cluster
│   │   │       │   ├── compose
│   │   │       │   ├── covariance
│   │   │       │   ├── cross_decomposition
│   │   │       │   ├── datasets
│   │   │       │   ├── decomposition
│   │   │       │   ├── ensemble
│   │   │       │   ├── experimental
│   │   │       │   ├── externals
│   │   │       │   ├── feature_extraction
│   │   │       │   ├── feature_selection
│   │   │       │   ├── frozen
│   │   │       │   ├── gaussian_process
│   │   │       │   ├── impute
│   │   │       │   ├── inspection
│   │   │       │   ├── linear_model
│   │   │       │   ├── manifold
│   │   │       │   ├── metrics
│   │   │       │   ├── mixture
│   │   │       │   ├── model_selection
│   │   │       │   ├── neighbors
│   │   │       │   ├── neural_network
│   │   │       │   ├── preprocessing
│   │   │       │   ├── semi_supervised
│   │   │       │   ├── svm
│   │   │       │   ├── tests
│   │   │       │   ├── tree
│   │   │       │   ├── utils
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _built_with_meson.py
│   │   │       │   ├── _config.py
│   │   │       │   ├── _cyutility.cp310-win_amd64.lib
│   │   │       │   ├── _cyutility.cp310-win_amd64.pyd
│   │   │       │   ├── _distributor_init.py
│   │   │       │   ├── _isotonic.cp310-win_amd64.lib
│   │   │       │   ├── _isotonic.cp310-win_amd64.pyd
│   │   │       │   ├── _isotonic.pyx
│   │   │       │   ├── _min_dependencies.py
│   │   │       │   ├── base.py
│   │   │       │   ├── calibration.py
│   │   │       │   ├── conftest.py
│   │   │       │   ├── discriminant_analysis.py
│   │   │       │   ├── dummy.py
│   │   │       │   ├── exceptions.py
│   │   │       │   ├── isotonic.py
│   │   │       │   ├── kernel_approximation.py
│   │   │       │   ├── kernel_ridge.py
│   │   │       │   ├── meson.build
│   │   │       │   ├── multiclass.py
│   │   │       │   ├── multioutput.py
│   │   │       │   ├── naive_bayes.py
│   │   │       │   ├── pipeline.py
│   │   │       │   └── random_projection.py
│   │   │       ├── soupsieve
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __meta__.py
│   │   │       │   ├── css_match.py
│   │   │       │   ├── css_parser.py
│   │   │       │   ├── css_types.py
│   │   │       │   ├── pretty.py
│   │   │       │   ├── py.typed
│   │   │       │   └── util.py
│   │   │       ├── soupsieve-2.9.1.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── stack_data
│   │   │       │   ├── __init__.py
│   │   │       │   ├── core.py
│   │   │       │   ├── formatting.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── serializing.py
│   │   │       │   ├── utils.py
│   │   │       │   └── version.py
│   │   │       ├── stack_data-0.6.3.dist-info
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE.txt
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── structlog
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _base.py
│   │   │       │   ├── _config.py
│   │   │       │   ├── _frames.py
│   │   │       │   ├── _generic.py
│   │   │       │   ├── _greenlets.py
│   │   │       │   ├── _log_levels.py
│   │   │       │   ├── _native.py
│   │   │       │   ├── _output.py
│   │   │       │   ├── _utils.py
│   │   │       │   ├── contextvars.py
│   │   │       │   ├── dev.py
│   │   │       │   ├── exceptions.py
│   │   │       │   ├── processors.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── stdlib.py
│   │   │       │   ├── testing.py
│   │   │       │   ├── threadlocal.py
│   │   │       │   ├── tracebacks.py
│   │   │       │   ├── twisted.py
│   │   │       │   ├── types.py
│   │   │       │   └── typing.py
│   │   │       ├── structlog-26.1.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── studio
│   │   │       │   ├── backend
│   │   │       │   ├── frontend
│   │   │       │   ├── src-tauri
│   │   │       │   ├── __init__.py
│   │   │       │   ├── install_llama_prebuilt.py
│   │   │       │   ├── install_manifest.py
│   │   │       │   ├── install_node_prebuilt.py
│   │   │       │   ├── install_python_stack.py
│   │   │       │   ├── install_sd_cpp_prebuilt.py
│   │   │       │   ├── install_whisper_prebuilt.py
│   │   │       │   ├── LICENSE.AGPL-3.0
│   │   │       │   ├── MCP.md
│   │   │       │   ├── node_prebuilt_pins.json
│   │   │       │   ├── package-lock.json
│   │   │       │   ├── package.json
│   │   │       │   ├── prebuilt_core.py
│   │   │       │   ├── setup.bat
│   │   │       │   ├── setup.ps1
│   │   │       │   ├── setup.sh
│   │   │       │   └── Unsloth_Studio_Colab.ipynb
│   │   │       ├── sympy
│   │   │       │   ├── algebras
│   │   │       │   ├── assumptions
│   │   │       │   ├── benchmarks
│   │   │       │   ├── calculus
│   │   │       │   ├── categories
│   │   │       │   ├── codegen
│   │   │       │   ├── combinatorics
│   │   │       │   ├── concrete
│   │   │       │   ├── core
│   │   │       │   ├── crypto
│   │   │       │   ├── diffgeom
│   │   │       │   ├── discrete
│   │   │       │   ├── external
│   │   │       │   ├── functions
│   │   │       │   ├── geometry
│   │   │       │   ├── holonomic
│   │   │       │   ├── integrals
│   │   │       │   ├── interactive
│   │   │       │   ├── liealgebras
│   │   │       │   ├── logic
│   │   │       │   ├── matrices
│   │   │       │   ├── multipledispatch
│   │   │       │   ├── ntheory
│   │   │       │   ├── parsing
│   │   │       │   ├── physics
│   │   │       │   ├── plotting
│   │   │       │   ├── polys
│   │   │       │   ├── printing
│   │   │       │   ├── sandbox
│   │   │       │   ├── series
│   │   │       │   ├── sets
│   │   │       │   ├── simplify
│   │   │       │   ├── solvers
│   │   │       │   ├── stats
│   │   │       │   ├── strategies
│   │   │       │   ├── tensor
│   │   │       │   ├── testing
│   │   │       │   ├── unify
│   │   │       │   ├── utilities
│   │   │       │   ├── vector
│   │   │       │   ├── __init__.py
│   │   │       │   ├── abc.py
│   │   │       │   ├── conftest.py
│   │   │       │   ├── galgebra.py
│   │   │       │   ├── release.py
│   │   │       │   └── this.py
│   │   │       ├── sympy-1.14.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── terminado
│   │   │       │   ├── _static
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _version.py
│   │   │       │   ├── management.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── uimod_embed.js
│   │   │       │   ├── uimodule.py
│   │   │       │   └── websocket.py
│   │   │       ├── terminado-0.18.1.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── test
│   │   │       │   ├── prototype
│   │   │       │   ├── __init__.py
│   │   │       │   ├── conftest.py
│   │   │       │   ├── test_lean_import.py
│   │   │       │   ├── test_low_bit_optim.py
│   │   │       │   ├── test_model_architecture.py
│   │   │       │   ├── test_ops.py
│   │   │       │   └── test_utils.py
│   │   │       ├── tests
│   │   │       │   ├── mlx_simulation
│   │   │       │   ├── security
│   │   │       │   ├── _merge_e2e_helpers.py
│   │   │       │   ├── _pickle_base.py
│   │   │       │   ├── conftest.py
│   │   │       │   ├── gemma4_audio_version_probe.py
│   │   │       │   ├── test_active_merge_device_matrix.py
│   │   │       │   ├── test_add_new_tokens_padded_vocab.py
│   │   │       │   ├── test_alloc_conf_platform_matrix.py
│   │   │       │   ├── test_assert_same_keys_base_model.py
│   │   │       │   ├── test_backend_device_helpers.py
│   │   │       │   ├── test_bin_only_base_diagnosis.py
│   │   │       │   ├── test_check_hf_model_exists_transport_errors.py
│   │   │       │   ├── test_compile_cache_security.py
│   │   │       │   ├── test_compile_disable_partial.py
│   │   │       │   ├── test_compiler_decorated_forward.py
│   │   │       │   ├── test_compiler_dynamic_exec.py
│   │   │       │   ├── test_compiler_output_capture.py
│   │   │       │   ├── test_compiler_rewriter_exhaustive.py
│   │   │       │   ├── test_convert_hf_to_gguf_patcher.py
│   │   │       │   ├── test_convert_to_gguf_mtp_reconcile.py
│   │   │       │   ├── test_convert_to_gguf_self_heal.py
│   │   │       │   ├── test_cross_entropy_chunk_cap.py
│   │   │       │   ├── test_dataset_num_proc.py
│   │   │       │   ├── test_datasets_map_worker_death_retry.py
│   │   │       │   ├── test_deepseek_v2_moe_alias.py
│   │   │       │   ├── test_diffusion_canvas_maxtok.py
│   │   │       │   ├── test_diffusion_shim_thought_split.py
│   │   │       │   ├── test_diffusion_visual_engine_env.py
│   │   │       │   ├── test_disabled_hook_graph_break.py
│   │   │       │   ├── test_dora_merge.py
│   │   │       │   ├── test_eager_fallback_latch.py
│   │   │       │   ├── test_encode_conversations_with_harmony_render.py
│   │   │       │   ├── test_encode_conversations_with_harmony.py
│   │   │       │   ├── test_extended_dep_api_pins.py
│   │   │       │   ├── test_file_uri_resolution.py
│   │   │       │   ├── test_find_common_token_ids_no_match.py
│   │   │       │   ├── test_forward_native_moe_loop_lora.py
│   │   │       │   ├── test_fp8_dense_merge.py
│   │   │       │   ├── test_fused_forward_install.py
│   │   │       │   ├── test_gated_and_offline_config_classification.py
│   │   │       │   ├── test_gemma3_processor_batched.py
│   │   │       │   ├── test_gemma4_audio_dtype.py
│   │   │       │   ├── test_gemma4_banded_attention.py
│   │   │       │   ├── test_gemma4_clippable_linear_peft_reload.py
│   │   │       │   ├── test_gemma4_dtype_drift_guards.py
│   │   │       │   ├── test_gemma4_flash_sliding.py
│   │   │       │   ├── test_gemma4_forced_float32_ple_dtype.py
│   │   │       │   ├── test_gemma4_moe_lora_registration.py
│   │   │       │   ├── test_gemma4_probe_two_tone_gate.py
│   │   │       │   ├── test_gemma4_vision_pooler_fp16.py
│   │   │       │   ├── test_generated_trainer_is_installed.py
│   │   │       │   ├── test_get_transformers_model_type_empty.py
│   │   │       │   ├── test_gguf_bitsandbytes_guard.py
│   │   │       │   ├── test_gguf_oom_temp_file_retry.py
│   │   │       │   ├── test_gpt_oss_attention_mask.py
│   │   │       │   ├── test_gptoss_grouped_gate.py
│   │   │       │   ├── test_grpo_chunked_reduction_dim.py
│   │   │       │   ├── test_grpo_packed_raw_logits_dispatch.py
│   │   │       │   ├── test_grpo_packed_verify_raw_logits.py
│   │   │       │   ├── test_hf_cache_redirect.py
│   │   │       │   ├── test_hf_transfer_windows_arm.py
│   │   │       │   ├── test_hf_xet_applies_automatically.py
│   │   │       │   ├── test_hf_xet_fallback.py
│   │   │       │   ├── test_hf_xet_health.py
│   │   │       │   ├── test_hf_xet_tuning.py
│   │   │       │   ├── test_hub_transport_errors_single_segment.py
│   │   │       │   ├── test_ignored_tokenizer_casing.py
│   │   │       │   ├── test_llama_cpp_bundle_converter.py
│   │   │       │   ├── test_llama_cpp_loader.py
│   │   │       │   ├── test_llama_cpp_prebuilt.py
│   │   │       │   ├── test_local_4bit_merge_offline_resolution.py
│   │   │       │   ├── test_local_base_model_resolution_offline.py
│   │   │       │   ├── test_local_fp8_base_offline_resolution.py
│   │   │       │   ├── test_longrope_attention_factor.py
│   │   │       │   ├── test_mamba_ssm_pre_ampere_fallback.py
│   │   │       │   ├── test_merge_e2e_dense.py
│   │   │       │   ├── test_merge_e2e_hub_unreachable.py
│   │   │       │   ├── test_merge_e2e_moe_fused.py
│   │   │       │   ├── test_merge_e2e_moe_per_expert.py
│   │   │       │   ├── test_merge_e2e_resized.py
│   │   │       │   ├── test_merge_e2e_vision_passthrough.py
│   │   │       │   ├── test_mlx_adapter_metadata_persistence.py
│   │   │       │   ├── test_mlx_autodetect_template_source.py
│   │   │       │   ├── test_mlx_baseline_loss_parity.py
│   │   │       │   ├── test_mlx_batch_padding.py
│   │   │       │   ├── test_mlx_batching_and_decay.py
│   │   │       │   ├── test_mlx_cce_kernel.py
│   │   │       │   ├── test_mlx_cce_target_classification.py
│   │   │       │   ├── test_mlx_cpt_partition_metal.py
│   │   │       │   ├── test_mlx_ddp_metal.py
│   │   │       │   ├── test_mlx_dequantize_modules.py
│   │   │       │   ├── test_mlx_distributed_loader.py
│   │   │       │   ├── test_mlx_double_quant_reject.py
│   │   │       │   ├── test_mlx_dtype_downcast_warning.py
│   │   │       │   ├── test_mlx_extra_special_tokens_compat.py
│   │   │       │   ├── test_mlx_finetune_last_n_layers.py
│   │   │       │   ├── test_mlx_gated_delta_batch_grad.py
│   │   │       │   ├── test_mlx_gated_delta_vjp.py
│   │   │       │   ├── test_mlx_gated_delta.py
│   │   │       │   ├── test_mlx_generate_metal.py
│   │   │       │   ├── test_mlx_generate.py
│   │   │       │   ├── test_mlx_get_peft_model_seed_ordering.py
│   │   │       │   ├── test_mlx_grad_clip_resolution.py
│   │   │       │   ├── test_mlx_module_exports.py
│   │   │       │   ├── test_mlx_neftune_quant_map.py
│   │   │       │   ├── test_mlx_platform_spoof_is_scoped.py
│   │   │       │   ├── test_mlx_pr684_full_validation_metal.py
│   │   │       │   ├── test_mlx_preference.py
│   │   │       │   ├── test_mlx_qk_norm_version_gap.py
│   │   │       │   ├── test_mlx_quantized_optimizer_routing.py
│   │   │       │   ├── test_mlx_quantized_optimizer_state.py
│   │   │       │   ├── test_mlx_qwen3_prompt_batch_isolated.py
│   │   │       │   ├── test_mlx_runtime_cce_compile.py
│   │   │       │   ├── test_mlx_save_export_edge_cases.py
│   │   │       │   ├── test_mlx_save_export_regressions.py
│   │   │       │   ├── test_mlx_save_lora_adapters_filter.py
│   │   │       │   ├── test_mlx_shape_guard.py
│   │   │       │   ├── test_mlx_switch_lora.py
│   │   │       │   ├── test_mlx_tokenizer_utils_torch_free.py
│   │   │       │   ├── test_mlx_torch_shim_smoke.py
│   │   │       │   ├── test_mlx_trainer_internals.py
│   │   │       │   ├── test_mlx_training_e2e_metal.py
│   │   │       │   ├── test_mlx_vlm_label_masks.py
│   │   │       │   ├── test_moe_bnb4bit_adaptive_recompute.py
│   │   │       │   ├── test_moe_bnb4bit_per_expert_conversions.py
│   │   │       │   ├── test_moe_fused_baddbmm_equiv.py
│   │   │       │   ├── test_moe_fused_narrow_expert_merge.py
│   │   │       │   ├── test_moe_gategrad_identity.py
│   │   │       │   ├── test_moe_grouped_mm_alignment_fallback.py
│   │   │       │   ├── test_moe_grouped_mm_format.py
│   │   │       │   ├── test_moe_grouped_mm_no_copy.py
│   │   │       │   ├── test_moe_grouped_modulelist_parity.py
│   │   │       │   ├── test_moe_lora_extractor_coverage.py
│   │   │       │   ├── test_moe_merge_e2e_cpu.py
│   │   │       │   ├── test_moe_merge_legacy_mixtral_cpu.py
│   │   │       │   ├── test_moe_num_experts_header_precedence.py
│   │   │       │   ├── test_moe_preprocess_weight_transpose.py
│   │   │       │   ├── test_moe_quant_cleanup.py
│   │   │       │   ├── test_moe_quant_handler_registry.py
│   │   │       │   ├── test_moe_recompute_gc_adaptive.py
│   │   │       │   ├── test_mxfp4_convert_no_double_transpose.py
│   │   │       │   ├── test_mxfp4_import_resilient.py
│   │   │       │   ├── test_mxfp4_transpose_convention.py
│   │   │       │   ├── test_notebook_chat_templates.py
│   │   │       │   ├── test_offline_env_cross_sync.py
│   │   │       │   ├── test_pad_token.py
│   │   │       │   ├── test_patch_loss_functions_coverage.py
│   │   │       │   ├── test_peft_paramwrapper_layout_drift.py
│   │   │       │   ├── test_peft_regex_audio.py
│   │   │       │   ├── test_pr684_review_fixes_a.py
│   │   │       │   ├── test_pr684_review_fixes_b.py
│   │   │       │   ├── test_prepare_model_for_training_bias.py
│   │   │       │   ├── test_prepare_model_for_training_fp32_norms.py
│   │   │       │   ├── test_pypi_version_sync.py
│   │   │       │   ├── test_python39_compatibility.py
│   │   │       │   ├── test_quant_status_transport_errors.py
│   │   │       │   ├── test_quantize_gguf_q2_k_l.py
│   │   │       │   ├── test_qwen_moe_lora_extractor.py
│   │   │       │   ├── test_qwen35_ssm_tensor_mapping.py
│   │   │       │   ├── test_qwen35_vjp_metal.py
│   │   │       │   ├── test_reasoning_marker_strip.py
│   │   │       │   ├── test_recompile_limit_fallback.py
│   │   │       │   ├── test_requires_grad_hook_dynamo.py
│   │   │       │   ├── test_resized_shard_rewrite_parity.py
│   │   │       │   ├── test_rl_replacements_compile_disable.py
│   │   │       │   ├── test_rl_replacements_cpu.py
│   │   │       │   ├── test_rmsnorm_recompile_guards.py
│   │   │       │   ├── test_saving_utils_lora_remap_count.py
│   │   │       │   ├── test_saving_utils_quant_aware_merge.py
│   │   │       │   ├── test_sft_prepare_dataset_double_bos.py
│   │   │       │   ├── test_streaming_map_batch_size.py
│   │   │       │   ├── test_temporary_patches_exhaustive.py
│   │   │       │   ├── test_temporary_patches_imports.py
│   │   │       │   ├── test_tiled_mlp_target_gb.py
│   │   │       │   ├── test_train_on_responses_list_labels.py
│   │   │       │   ├── test_training_utils_use_cache.py
│   │   │       │   ├── test_transformers_moe_structure_drift.py
│   │   │       │   ├── test_triton_stub_class_symbols.py
│   │   │       │   ├── test_trl_entropy_metric.py
│   │   │       │   ├── test_trl_sft_logits_metrics.py
│   │   │       │   ├── test_unreadable_modeling_source.py
│   │   │       │   ├── test_unsloth_zoo_lora_merge.py
│   │   │       │   ├── test_upstream_import_fixes_drift.py
│   │   │       │   ├── test_upstream_pinned_symbols_accelerator.py
│   │   │       │   ├── test_upstream_pinned_symbols_transformers.py
│   │   │       │   ├── test_upstream_pinned_symbols_trl_vllm.py
│   │   │       │   ├── test_upstream_signatures.py
│   │   │       │   ├── test_upstream_source_patterns.py
│   │   │       │   ├── test_vendor_fla.py
│   │   │       │   ├── test_vendored_license_shipped.py
│   │   │       │   ├── test_vision_collator_audio.py
│   │   │       │   ├── test_vision_collator_prompt_completion.py
│   │   │       │   ├── test_vllm_direct_lora_loading.py
│   │   │       │   ├── test_vllm_flashinfer_hip.py
│   │   │       │   ├── test_vllm_lora_unstacked_mapper.py
│   │   │       │   ├── test_vllm_sleep_cache_reset.py
│   │   │       │   ├── test_vllm_to_hf_conversion.py
│   │   │       │   ├── test_vllm_utils_xpu_sm_cap.py
│   │   │       │   ├── test_vlm_collator_masking.py
│   │   │       │   ├── test_vlm_token_coverage.py
│   │   │       │   ├── test_zephyr_marker_context.py
│   │   │       │   ├── test_zoo_history_regressions_deep.py
│   │   │       │   ├── test_zoo_history_regressions.py
│   │   │       │   └── test_zoo_source_upstream_refs.py
│   │   │       ├── threadpoolctl-3.6.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── tiktoken
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _educational.py
│   │   │       │   ├── _tiktoken.cp310-win_amd64.pyd
│   │   │       │   ├── core.py
│   │   │       │   ├── load.py
│   │   │       │   ├── model.py
│   │   │       │   ├── py.typed
│   │   │       │   └── registry.py
│   │   │       ├── tiktoken_ext
│   │   │       │   └── openai_public.py
│   │   │       ├── tiktoken-0.13.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── tinycss2
│   │   │       │   ├── __init__.py
│   │   │       │   ├── ast.py
│   │   │       │   ├── bytes.py
│   │   │       │   ├── color3.py
│   │   │       │   ├── color4.py
│   │   │       │   ├── color5.py
│   │   │       │   ├── nth.py
│   │   │       │   ├── parser.py
│   │   │       │   ├── serializer.py
│   │   │       │   └── tokenizer.py
│   │   │       ├── tinycss2-1.5.1.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── tokenizers
│   │   │       │   ├── decoders
│   │   │       │   ├── implementations
│   │   │       │   ├── models
│   │   │       │   ├── normalizers
│   │   │       │   ├── pre_tokenizers
│   │   │       │   ├── processors
│   │   │       │   ├── tools
│   │   │       │   ├── trainers
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __init__.pyi
│   │   │       │   ├── tokenizers.pyd
│   │   │       │   └── tokenizers.pyi
│   │   │       ├── tokenizers-0.22.2.dist-info
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── tomli
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _parser.py
│   │   │       │   ├── _re.py
│   │   │       │   ├── _types.py
│   │   │       │   └── py.typed
│   │   │       ├── tomli-2.4.1.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── torch
│   │   │       │   ├── _awaits
│   │   │       │   ├── _C
│   │   │       │   ├── _C_flatbuffer
│   │   │       │   ├── _custom_op
│   │   │       │   ├── _decomp
│   │   │       │   ├── _dispatch
│   │   │       │   ├── _dynamo
│   │   │       │   ├── _export
│   │   │       │   ├── _functorch
│   │   │       │   ├── _higher_order_ops
│   │   │       │   ├── _inductor
│   │   │       │   ├── _lazy
│   │   │       │   ├── _library
│   │   │       │   ├── _logging
│   │   │       │   ├── _numpy
│   │   │       │   ├── _prims
│   │   │       │   ├── _prims_common
│   │   │       │   ├── _refs
│   │   │       │   ├── _strobelight
│   │   │       │   ├── _subclasses
│   │   │       │   ├── _vendor
│   │   │       │   ├── accelerator
│   │   │       │   ├── amp
│   │   │       │   ├── ao
│   │   │       │   ├── autograd
│   │   │       │   ├── backends
│   │   │       │   ├── bin
│   │   │       │   ├── compiler
│   │   │       │   ├── contrib
│   │   │       │   ├── cpu
│   │   │       │   ├── csrc
│   │   │       │   ├── cuda
│   │   │       │   ├── distributed
│   │   │       │   ├── distributions
│   │   │       │   ├── export
│   │   │       │   ├── fft
│   │   │       │   ├── func
│   │   │       │   ├── futures
│   │   │       │   ├── fx
│   │   │       │   ├── include
│   │   │       │   ├── jit
│   │   │       │   ├── lib
│   │   │       │   ├── linalg
│   │   │       │   ├── masked
│   │   │       │   ├── monitor
│   │   │       │   ├── mps
│   │   │       │   ├── mtia
│   │   │       │   ├── multiprocessing
│   │   │       │   ├── nativert
│   │   │       │   ├── nested
│   │   │       │   ├── nn
│   │   │       │   ├── numa
│   │   │       │   ├── onnx
│   │   │       │   ├── optim
│   │   │       │   ├── package
│   │   │       │   ├── profiler
│   │   │       │   ├── quantization
│   │   │       │   ├── share
│   │   │       │   ├── signal
│   │   │       │   ├── sparse
│   │   │       │   ├── special
│   │   │       │   ├── testing
│   │   │       │   ├── utils
│   │   │       │   ├── xpu
│   │   │       │   ├── __config__.py
│   │   │       │   ├── __future__.py
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _appdirs.py
│   │   │       │   ├── _C.cp310-win_amd64.pyd
│   │   │       │   ├── _classes.py
│   │   │       │   ├── _compile.py
│   │   │       │   ├── _custom_ops.py
│   │   │       │   ├── _environment.py
│   │   │       │   ├── _guards.py
│   │   │       │   ├── _jit_internal.py
│   │   │       │   ├── _linalg_utils.py
│   │   │       │   ├── _lobpcg.py
│   │   │       │   ├── _lowrank.py
│   │   │       │   ├── _meta_registrations.py
│   │   │       │   ├── _namedtensor_internals.py
│   │   │       │   ├── _opaque_base.py
│   │   │       │   ├── _ops.py
│   │   │       │   ├── _python_dispatcher.py
│   │   │       │   ├── _size_docs.py
│   │   │       │   ├── _sources.py
│   │   │       │   ├── _storage_docs.py
│   │   │       │   ├── _streambase.py
│   │   │       │   ├── _tensor_docs.py
│   │   │       │   ├── _tensor_str.py
│   │   │       │   ├── _tensor.py
│   │   │       │   ├── _thread_safe_fork.py
│   │   │       │   ├── _torch_docs.py
│   │   │       │   ├── _utils_internal.py
│   │   │       │   ├── _utils.py
│   │   │       │   ├── _VF.py
│   │   │       │   ├── _VF.pyi
│   │   │       │   ├── _vmap_internals.py
│   │   │       │   ├── _weights_only_unpickler.py
│   │   │       │   ├── functional.py
│   │   │       │   ├── hub.py
│   │   │       │   ├── library.py
│   │   │       │   ├── overrides.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── quasirandom.py
│   │   │       │   ├── random.py
│   │   │       │   ├── return_types.py
│   │   │       │   ├── return_types.pyi
│   │   │       │   ├── serialization.py
│   │   │       │   ├── storage.py
│   │   │       │   ├── torch_version.py
│   │   │       │   ├── types.py
│   │   │       │   └── version.py
│   │   │       ├── torch-2.11.0+cu128.dist-info
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE
│   │   │       │   ├── METADATA
│   │   │       │   ├── NOTICE
│   │   │       │   ├── RECORD
│   │   │       │   ├── REQUESTED
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── torchao
│   │   │       │   ├── _models
│   │   │       │   ├── core
│   │   │       │   ├── dtypes
│   │   │       │   ├── experimental
│   │   │       │   ├── float8
│   │   │       │   ├── kernel
│   │   │       │   ├── optim
│   │   │       │   ├── prototype
│   │   │       │   ├── quantization
│   │   │       │   ├── sparsity
│   │   │       │   ├── swizzle
│   │   │       │   ├── testing
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _executorch_ops.py
│   │   │       │   ├── csrc_meta_ops.py
│   │   │       │   ├── ops.py
│   │   │       │   └── utils.py
│   │   │       ├── torchao-0.18.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── torchaudio
│   │   │       │   ├── _extension
│   │   │       │   ├── _internal
│   │   │       │   ├── compliance
│   │   │       │   ├── datasets
│   │   │       │   ├── functional
│   │   │       │   ├── lib
│   │   │       │   ├── models
│   │   │       │   ├── pipelines
│   │   │       │   ├── transforms
│   │   │       │   ├── utils
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _torchcodec.py
│   │   │       │   └── version.py
│   │   │       ├── torchaudio-2.11.0+cu128.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── REQUESTED
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── torchgen
│   │   │       │   ├── aoti
│   │   │       │   ├── api
│   │   │       │   ├── dest
│   │   │       │   ├── operator_versions
│   │   │       │   ├── packaged
│   │   │       │   ├── selective_build
│   │   │       │   ├── static_runtime
│   │   │       │   ├── __init__.py
│   │   │       │   ├── code_template.py
│   │   │       │   ├── context.py
│   │   │       │   ├── gen_aoti_c_shim.py
│   │   │       │   ├── gen_backend_stubs.py
│   │   │       │   ├── gen_functionalization_type.py
│   │   │       │   ├── gen_lazy_tensor.py
│   │   │       │   ├── gen_schema_utils.py
│   │   │       │   ├── gen_vmap_plumbing.py
│   │   │       │   ├── gen.py
│   │   │       │   ├── local.py
│   │   │       │   ├── model.py
│   │   │       │   ├── native_function_generation.py
│   │   │       │   ├── utils.py
│   │   │       │   └── yaml_utils.py
│   │   │       ├── torchvision
│   │   │       │   ├── datasets
│   │   │       │   ├── io
│   │   │       │   ├── models
│   │   │       │   ├── ops
│   │   │       │   ├── transforms
│   │   │       │   ├── tv_tensors
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _C.pyd
│   │   │       │   ├── _internally_replaced_utils.py
│   │   │       │   ├── _meta_registrations.py
│   │   │       │   ├── _utils.py
│   │   │       │   ├── cudart64_12.dll
│   │   │       │   ├── extension.py
│   │   │       │   ├── image.pyd
│   │   │       │   ├── jpeg8.dll
│   │   │       │   ├── libjpeg.dll
│   │   │       │   ├── libpng16.dll
│   │   │       │   ├── libsharpyuv.dll
│   │   │       │   ├── libwebp.dll
│   │   │       │   ├── nvjpeg64_12.dll
│   │   │       │   ├── python310.dll
│   │   │       │   ├── utils.py
│   │   │       │   ├── version.py
│   │   │       │   └── zlib.dll
│   │   │       ├── torchvision-0.26.0+cu128.dist-info
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── REQUESTED
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── tornado
│   │   │       │   ├── platform
│   │   │       │   ├── test
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __init__.pyi
│   │   │       │   ├── _locale_data.py
│   │   │       │   ├── auth.py
│   │   │       │   ├── autoreload.py
│   │   │       │   ├── concurrent.py
│   │   │       │   ├── curl_httpclient.py
│   │   │       │   ├── escape.py
│   │   │       │   ├── gen.py
│   │   │       │   ├── http1connection.py
│   │   │       │   ├── httpclient.py
│   │   │       │   ├── httpserver.py
│   │   │       │   ├── httputil.py
│   │   │       │   ├── ioloop.py
│   │   │       │   ├── iostream.py
│   │   │       │   ├── locale.py
│   │   │       │   ├── locks.py
│   │   │       │   ├── log.py
│   │   │       │   ├── netutil.py
│   │   │       │   ├── options.py
│   │   │       │   ├── process.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── queues.py
│   │   │       │   ├── routing.py
│   │   │       │   ├── simple_httpclient.py
│   │   │       │   ├── speedups.pyd
│   │   │       │   ├── speedups.pyi
│   │   │       │   ├── tcpclient.py
│   │   │       │   ├── tcpserver.py
│   │   │       │   ├── template.py
│   │   │       │   ├── testing.py
│   │   │       │   ├── util.py
│   │   │       │   ├── web.py
│   │   │       │   ├── websocket.py
│   │   │       │   └── wsgi.py
│   │   │       ├── tornado-6.5.7.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── tqdm
│   │   │       │   ├── contrib
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __main__.py
│   │   │       │   ├── _main.py
│   │   │       │   ├── _monitor.py
│   │   │       │   ├── _tqdm_gui.py
│   │   │       │   ├── _tqdm_notebook.py
│   │   │       │   ├── _tqdm_pandas.py
│   │   │       │   ├── _tqdm.py
│   │   │       │   ├── _utils.py
│   │   │       │   ├── asyncio.py
│   │   │       │   ├── auto.py
│   │   │       │   ├── autonotebook.py
│   │   │       │   ├── cli.py
│   │   │       │   ├── completion.sh
│   │   │       │   ├── dask.py
│   │   │       │   ├── gui.py
│   │   │       │   ├── keras.py
│   │   │       │   ├── notebook.py
│   │   │       │   ├── rich.py
│   │   │       │   ├── std.py
│   │   │       │   ├── tk.py
│   │   │       │   ├── tqdm.1
│   │   │       │   ├── utils.py
│   │   │       │   └── version.py
│   │   │       ├── tqdm-4.70.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── traitlets
│   │   │       │   ├── config
│   │   │       │   ├── tests
│   │   │       │   ├── utils
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _version.py
│   │   │       │   ├── log.py
│   │   │       │   ├── py.typed
│   │   │       │   └── traitlets.py
│   │   │       ├── traitlets-5.16.1.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── transformers
│   │   │       │   ├── cli
│   │   │       │   ├── data
│   │   │       │   ├── distributed
│   │   │       │   ├── generation
│   │   │       │   ├── integrations
│   │   │       │   ├── loss
│   │   │       │   ├── models
│   │   │       │   ├── pipelines
│   │   │       │   ├── quantizers
│   │   │       │   ├── utils
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _typing.py
│   │   │       │   ├── activations.py
│   │   │       │   ├── audio_utils.py
│   │   │       │   ├── backbone_utils.py
│   │   │       │   ├── cache_utils.py
│   │   │       │   ├── configuration_utils.py
│   │   │       │   ├── conversion_mapping.py
│   │   │       │   ├── convert_slow_tokenizer.py
│   │   │       │   ├── convert_slow_tokenizers_checkpoints_to_fast.py
│   │   │       │   ├── core_model_loading.py
│   │   │       │   ├── debug_utils.py
│   │   │       │   ├── dependency_versions_check.py
│   │   │       │   ├── dependency_versions_table.py
│   │   │       │   ├── dynamic_module_utils.py
│   │   │       │   ├── feature_extraction_sequence_utils.py
│   │   │       │   ├── feature_extraction_utils.py
│   │   │       │   ├── file_utils.py
│   │   │       │   ├── hf_argparser.py
│   │   │       │   ├── hyperparameter_search.py
│   │   │       │   ├── image_processing_backends.py
│   │   │       │   ├── image_processing_base.py
│   │   │       │   ├── image_processing_utils.py
│   │   │       │   ├── image_transforms.py
│   │   │       │   ├── image_utils.py
│   │   │       │   ├── initialization.py
│   │   │       │   ├── masking_utils.py
│   │   │       │   ├── model_debugging_utils.py
│   │   │       │   ├── modelcard.py
│   │   │       │   ├── modeling_attn_mask_utils.py
│   │   │       │   ├── modeling_flash_attention_utils.py
│   │   │       │   ├── modeling_gguf_pytorch_utils.py
│   │   │       │   ├── modeling_layers.py
│   │   │       │   ├── modeling_outputs.py
│   │   │       │   ├── modeling_rope_utils.py
│   │   │       │   ├── modeling_utils.py
│   │   │       │   ├── monkey_patching.py
│   │   │       │   ├── optimization.py
│   │   │       │   ├── processing_utils.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── pytorch_utils.py
│   │   │       │   ├── safetensors_conversion.py
│   │   │       │   ├── testing_utils.py
│   │   │       │   ├── time_series_utils.py
│   │   │       │   ├── tokenization_mistral_common.py
│   │   │       │   ├── tokenization_python.py
│   │   │       │   ├── tokenization_utils_base.py
│   │   │       │   ├── tokenization_utils_sentencepiece.py
│   │   │       │   ├── tokenization_utils_tokenizers.py
│   │   │       │   ├── trainer_callback.py
│   │   │       │   ├── trainer_jit_checkpoint.py
│   │   │       │   ├── trainer_optimizer.py
│   │   │       │   ├── trainer_pt_utils.py
│   │   │       │   ├── trainer_seq2seq.py
│   │   │       │   ├── trainer_utils.py
│   │   │       │   ├── trainer.py
│   │   │       │   ├── training_args_seq2seq.py
│   │   │       │   ├── training_args.py
│   │   │       │   ├── video_processing_utils.py
│   │   │       │   └── video_utils.py
│   │   │       ├── transformers-5.5.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── triton
│   │   │       │   ├── _C
│   │   │       │   ├── backends
│   │   │       │   ├── compiler
│   │   │       │   ├── experimental
│   │   │       │   ├── language
│   │   │       │   ├── runtime
│   │   │       │   ├── tools
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _filecheck.py
│   │   │       │   ├── _internal_testing.py
│   │   │       │   ├── _utils.py
│   │   │       │   ├── errors.py
│   │   │       │   ├── knobs.py
│   │   │       │   ├── testing.py
│   │   │       │   └── windows_utils.py
│   │   │       ├── triton_windows-3.7.1.post27.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── trl
│   │   │       │   ├── accelerate_configs
│   │   │       │   ├── experimental
│   │   │       │   ├── extras
│   │   │       │   ├── models
│   │   │       │   ├── rewards
│   │   │       │   ├── scripts
│   │   │       │   ├── templates
│   │   │       │   ├── trainer
│   │   │       │   ├── __init__.py
│   │   │       │   ├── cli.py
│   │   │       │   ├── core.py
│   │   │       │   ├── data_utils.py
│   │   │       │   ├── import_utils.py
│   │   │       │   ├── mergekit_utils.py
│   │   │       │   └── py.typed
│   │   │       ├── trl-0.24.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── REQUESTED
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── txt2tags-3.9.dist-info
│   │   │       │   ├── COPYING
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── typeguard
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _checkers.py
│   │   │       │   ├── _config.py
│   │   │       │   ├── _decorators.py
│   │   │       │   ├── _exceptions.py
│   │   │       │   ├── _functions.py
│   │   │       │   ├── _importhook.py
│   │   │       │   ├── _memo.py
│   │   │       │   ├── _pytest_plugin.py
│   │   │       │   ├── _suppression.py
│   │   │       │   ├── _transformer.py
│   │   │       │   ├── _utils.py
│   │   │       │   └── py.typed
│   │   │       ├── typeguard-4.6.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── typer
│   │   │       │   ├── _click
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __main__.py
│   │   │       │   ├── _completion_classes.py
│   │   │       │   ├── _completion_shared.py
│   │   │       │   ├── _types.py
│   │   │       │   ├── _typing.py
│   │   │       │   ├── cli.py
│   │   │       │   ├── colors.py
│   │   │       │   ├── completion.py
│   │   │       │   ├── core.py
│   │   │       │   ├── main.py
│   │   │       │   ├── models.py
│   │   │       │   ├── params.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── rich_utils.py
│   │   │       │   ├── testing.py
│   │   │       │   └── utils.py
│   │   │       ├── typer-0.27.1.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── typing_extensions-4.15.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── typing_inspection
│   │   │       │   ├── __init__.py
│   │   │       │   ├── introspection.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── typing_objects.py
│   │   │       │   └── typing_objects.pyi
│   │   │       ├── typing_inspection-0.4.2.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── tyro
│   │   │       │   ├── _backends
│   │   │       │   ├── conf
│   │   │       │   ├── constructors
│   │   │       │   ├── extras
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _arguments.py
│   │   │       │   ├── _calling.py
│   │   │       │   ├── _cli.py
│   │   │       │   ├── _deprecated.py
│   │   │       │   ├── _docstrings.py
│   │   │       │   ├── _errors.py
│   │   │       │   ├── _fields.py
│   │   │       │   ├── _fmtlib.py
│   │   │       │   ├── _parsers.py
│   │   │       │   ├── _resolver.py
│   │   │       │   ├── _settings.py
│   │   │       │   ├── _singleton.py
│   │   │       │   ├── _strings.py
│   │   │       │   ├── _subcommand_matching.py
│   │   │       │   ├── _typing_compat.py
│   │   │       │   ├── _unsafe_cache.py
│   │   │       │   ├── _warnings.py
│   │   │       │   └── py.typed
│   │   │       ├── tyro-1.0.15.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── tzdata
│   │   │       │   ├── zoneinfo
│   │   │       │   ├── __init__.py
│   │   │       │   └── zones
│   │   │       ├── tzdata-2026.3.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── unsloth
│   │   │       │   ├── dataprep
│   │   │       │   ├── kernels
│   │   │       │   ├── models
│   │   │       │   ├── optimizers
│   │   │       │   ├── registry
│   │   │       │   ├── utils
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _auto_install.py
│   │   │       │   ├── _compressed_quantize.py
│   │   │       │   ├── _gpu_init.py
│   │   │       │   ├── bnb_availability.py
│   │   │       │   ├── chat_templates.py
│   │   │       │   ├── dataset_num_proc.py
│   │   │       │   ├── device_type.py
│   │   │       │   ├── import_fixes.py
│   │   │       │   ├── ollama_template_mappers.py
│   │   │       │   ├── save.py
│   │   │       │   ├── tokenizer_utils.py
│   │   │       │   └── trainer.py
│   │   │       ├── unsloth_cli
│   │   │       │   ├── commands
│   │   │       │   ├── tests
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _inference.py
│   │   │       │   ├── _studio_deps.py
│   │   │       │   ├── _tool_policy.py
│   │   │       │   ├── claude_subagent_mcp.py
│   │   │       │   ├── codex_fallback_prompt.md
│   │   │       │   ├── codex_subagent_mcp.py
│   │   │       │   ├── config.py
│   │   │       │   ├── options.py
│   │   │       │   └── pi_subagent.ts
│   │   │       ├── unsloth_compiled_cache
│   │   │       │   ├── moe_utils.py
│   │   │       │   ├── UnslothBCOTrainer.py
│   │   │       │   ├── UnslothCPOTrainer.py
│   │   │       │   ├── UnslothDPOTrainer.py
│   │   │       │   ├── UnslothGKDTrainer.py
│   │   │       │   ├── UnslothGRPOTrainer.py
│   │   │       │   ├── UnslothKTOTrainer.py
│   │   │       │   ├── UnslothNashMDTrainer.py
│   │   │       │   ├── UnslothOnlineDPOTrainer.py
│   │   │       │   ├── UnslothORPOTrainer.py
│   │   │       │   ├── UnslothPPOTrainer.py
│   │   │       │   ├── UnslothPRMTrainer.py
│   │   │       │   ├── UnslothRewardTrainer.py
│   │   │       │   ├── UnslothRLOOTrainer.py
│   │   │       │   ├── UnslothSFTTrainer.py
│   │   │       │   └── UnslothXPOTrainer.py
│   │   │       ├── unsloth_zoo
│   │   │       │   ├── _vendored
│   │   │       │   ├── diffusion_studio
│   │   │       │   ├── flex_attention
│   │   │       │   ├── fused_losses
│   │   │       │   ├── mlx
│   │   │       │   ├── stubs
│   │   │       │   ├── temporary_patches
│   │   │       │   ├── __init__.py
│   │   │       │   ├── compile_cache.py
│   │   │       │   ├── compiler_replacements.py
│   │   │       │   ├── compiler.py
│   │   │       │   ├── dataset_num_proc.py
│   │   │       │   ├── dataset_utils.py
│   │   │       │   ├── device_type.py
│   │   │       │   ├── empty_model.py
│   │   │       │   ├── gated_delta_vjp.py
│   │   │       │   ├── gradient_checkpointing.py
│   │   │       │   ├── hf_cache_state.py
│   │   │       │   ├── hf_cache.py
│   │   │       │   ├── hf_utils.py
│   │   │       │   ├── hf_xet_fallback.py
│   │   │       │   ├── hf_xet_health.py
│   │   │       │   ├── hf_xet_tuning.py
│   │   │       │   ├── llama_cpp.py
│   │   │       │   ├── log.py
│   │   │       │   ├── logging_utils.py
│   │   │       │   ├── loss_utils.py
│   │   │       │   ├── model_lists.py
│   │   │       │   ├── pad_token.py
│   │   │       │   ├── patch_torch_functions.py
│   │   │       │   ├── patching_utils.py
│   │   │       │   ├── peft_utils.py
│   │   │       │   ├── rl_environments.py
│   │   │       │   ├── rl_replacements.py
│   │   │       │   ├── saving_utils.py
│   │   │       │   ├── tiled_mlp.py
│   │   │       │   ├── tokenizer_utils.py
│   │   │       │   ├── training_utils.py
│   │   │       │   ├── utils.py
│   │   │       │   ├── vision_utils.py
│   │   │       │   ├── vllm_lora_request.py
│   │   │       │   ├── vllm_lora_worker_manager.py
│   │   │       │   ├── vllm_rlhf_utils.py
│   │   │       │   ├── vllm_utils.py
│   │   │       │   └── vlm_tokens.py
│   │   │       ├── unsloth_zoo-2026.8.5.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── REQUESTED
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── unsloth-2026.8.7.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── REQUESTED
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── uri_template
│   │   │       │   ├── __init__.py
│   │   │       │   ├── charset.py
│   │   │       │   ├── expansions.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── uritemplate.py
│   │   │       │   └── variable.py
│   │   │       ├── uri_template-1.3.0.dist-info
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── urllib3
│   │   │       │   ├── contrib
│   │   │       │   ├── http2
│   │   │       │   ├── util
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _base_connection.py
│   │   │       │   ├── _collections.py
│   │   │       │   ├── _request_methods.py
│   │   │       │   ├── _version.py
│   │   │       │   ├── connection.py
│   │   │       │   ├── connectionpool.py
│   │   │       │   ├── exceptions.py
│   │   │       │   ├── fields.py
│   │   │       │   ├── filepost.py
│   │   │       │   ├── poolmanager.py
│   │   │       │   ├── py.typed
│   │   │       │   └── response.py
│   │   │       ├── urllib3-2.7.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── wcwidth
│   │   │       │   ├── table_grapheme_overrides
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _clip.py
│   │   │       │   ├── _constants.py
│   │   │       │   ├── _wcswidth.py
│   │   │       │   ├── _wcwidth.py
│   │   │       │   ├── _width.py
│   │   │       │   ├── align.py
│   │   │       │   ├── bisearch.py
│   │   │       │   ├── control_codes.py
│   │   │       │   ├── escape_sequences.py
│   │   │       │   ├── grapheme.py
│   │   │       │   ├── hyperlink.py
│   │   │       │   ├── py.typed
│   │   │       │   ├── sgr_state.py
│   │   │       │   ├── table_ambiguous.py
│   │   │       │   ├── table_grapheme.py
│   │   │       │   ├── table_mc.py
│   │   │       │   ├── table_overrides.py
│   │   │       │   ├── table_term_programs.py
│   │   │       │   ├── table_vs15.py
│   │   │       │   ├── table_vs16.py
│   │   │       │   ├── table_wide.py
│   │   │       │   ├── table_zero.py
│   │   │       │   ├── text_sizing.py
│   │   │       │   ├── textwrap.py
│   │   │       │   ├── unicode_versions.py
│   │   │       │   └── wcwidth.py
│   │   │       ├── wcwidth-0.8.2.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── webcolors
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _conversion.py
│   │   │       │   ├── _definitions.py
│   │   │       │   ├── _html5.py
│   │   │       │   ├── _normalization.py
│   │   │       │   └── _types.py
│   │   │       ├── webcolors-25.10.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── webencodings
│   │   │       │   ├── __init__.py
│   │   │       │   ├── labels.py
│   │   │       │   ├── mklabels.py
│   │   │       │   ├── tests.py
│   │   │       │   └── x_user_defined.py
│   │   │       ├── webencodings-0.5.1.dist-info
│   │   │       │   ├── DESCRIPTION.rst
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── metadata.json
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── websocket
│   │   │       │   ├── tests
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _abnf.py
│   │   │       │   ├── _app.py
│   │   │       │   ├── _cookiejar.py
│   │   │       │   ├── _core.py
│   │   │       │   ├── _dispatcher.py
│   │   │       │   ├── _exceptions.py
│   │   │       │   ├── _handshake.py
│   │   │       │   ├── _http.py
│   │   │       │   ├── _logging.py
│   │   │       │   ├── _socket.py
│   │   │       │   ├── _ssl_compat.py
│   │   │       │   ├── _url.py
│   │   │       │   ├── _utils.py
│   │   │       │   ├── _wsdump.py
│   │   │       │   └── py.typed
│   │   │       ├── websocket_client-1.9.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── wheel
│   │   │       │   ├── _commands
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __main__.py
│   │   │       │   ├── _bdist_wheel.py
│   │   │       │   ├── _metadata.py
│   │   │       │   ├── _setuptools_logging.py
│   │   │       │   ├── bdist_wheel.py
│   │   │       │   ├── macosx_libfile.py
│   │   │       │   ├── metadata.py
│   │   │       │   └── wheelfile.py
│   │   │       ├── wheel-0.47.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── entry_points.txt
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   └── WHEEL
│   │   │       ├── widgetsnbextension
│   │   │       │   ├── static
│   │   │       │   ├── __init__.py
│   │   │       │   └── _version.py
│   │   │       ├── widgetsnbextension-4.0.15.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── winpty
│   │   │       │   ├── tests
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _winpty.cp310-win_amd64.pyd
│   │   │       │   ├── _winpty.pyi
│   │   │       │   ├── conpty.dll
│   │   │       │   ├── enums.py
│   │   │       │   ├── OpenConsole.exe
│   │   │       │   ├── ptyprocess.py
│   │   │       │   ├── winpty-agent.exe
│   │   │       │   └── winpty.dll
│   │   │       ├── xformers
│   │   │       │   ├── benchmarks
│   │   │       │   ├── flash_attn_3
│   │   │       │   ├── ops
│   │   │       │   ├── profiler
│   │   │       │   ├── sparse
│   │   │       │   ├── triton
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _C.pyd
│   │   │       │   ├── _cpp_lib.py
│   │   │       │   ├── _deprecation_warning.py
│   │   │       │   ├── attn_bias_utils.py
│   │   │       │   ├── checkpoint.py
│   │   │       │   ├── cpp_lib.json
│   │   │       │   ├── fwbw_overlap.py
│   │   │       │   ├── info.py
│   │   │       │   ├── test.py
│   │   │       │   ├── utils.py
│   │   │       │   └── version.py
│   │   │       ├── xformers-0.0.35.dist-info
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── LICENSE
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── xxhash
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __init__.pyi
│   │   │       │   ├── _xxhash.cp310-win_amd64.pyd
│   │   │       │   ├── py.typed
│   │   │       │   └── version.py
│   │   │       ├── xxhash-3.8.1.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── yaml
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _yaml.cp310-win_amd64.pyd
│   │   │       │   ├── composer.py
│   │   │       │   ├── constructor.py
│   │   │       │   ├── cyaml.py
│   │   │       │   ├── dumper.py
│   │   │       │   ├── emitter.py
│   │   │       │   ├── error.py
│   │   │       │   ├── events.py
│   │   │       │   ├── loader.py
│   │   │       │   ├── nodes.py
│   │   │       │   ├── parser.py
│   │   │       │   ├── reader.py
│   │   │       │   ├── representer.py
│   │   │       │   ├── resolver.py
│   │   │       │   ├── scanner.py
│   │   │       │   ├── serializer.py
│   │   │       │   └── tokens.py
│   │   │       ├── yarl
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _parse.py
│   │   │       │   ├── _path.py
│   │   │       │   ├── _query.py
│   │   │       │   ├── _quoters.py
│   │   │       │   ├── _quoting_c.cp310-win_amd64.pyd
│   │   │       │   ├── _quoting_c.pyx
│   │   │       │   ├── _quoting_py.py
│   │   │       │   ├── _quoting.py
│   │   │       │   ├── _url.py
│   │   │       │   └── py.typed
│   │   │       ├── yarl-1.24.5.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── zipp
│   │   │       │   ├── compat
│   │   │       │   ├── __init__.py
│   │   │       │   ├── _functools.py
│   │   │       │   └── glob.py
│   │   │       ├── zipp-4.1.0.dist-info
│   │   │       │   ├── licenses
│   │   │       │   ├── INSTALLER
│   │   │       │   ├── METADATA
│   │   │       │   ├── RECORD
│   │   │       │   ├── top_level.txt
│   │   │       │   └── WHEEL
│   │   │       ├── zmq
│   │   │       │   ├── auth
│   │   │       │   ├── backend
│   │   │       │   ├── devices
│   │   │       │   ├── eventloop
│   │   │       │   ├── green
│   │   │       │   ├── log
│   │   │       │   ├── ssh
│   │   │       │   ├── sugar
│   │   │       │   ├── tests
│   │   │       │   ├── utils
│   │   │       │   ├── __init__.pxd
│   │   │       │   ├── __init__.py
│   │   │       │   ├── __init__.pyi
│   │   │       │   ├── _future.py
│   │   │       │   ├── _future.pyi
│   │   │       │   ├── _typing.py
│   │   │       │   ├── asyncio.py
│   │   │       │   ├── constants.py
│   │   │       │   ├── decorators.py
│   │   │       │   ├── error.py
│   │   │       │   └── py.typed
│   │   │       ├── _cffi_backend.cp310-win_amd64.pyd
│   │   │       ├── ada92cb5d92a588d1b93__mypyc.cp310-win_amd64.pyd
│   │   │       ├── distutils-precedence.pth
│   │   │       ├── ipykernel_launcher.py
│   │   │       ├── isympy.py
│   │   │       ├── jsonpointer.py
│   │   │       ├── jupyter.py
│   │   │       ├── nest_asyncio.py
│   │   │       ├── nest_asyncio2.py
│   │   │       ├── numpy-2.2.6-cp310-cp310-win_amd64.whl
│   │   │       ├── pandocfilters.py
│   │   │       ├── pylab.py
│   │   │       ├── rfc3339_validator.py
│   │   │       ├── rfc3986_validator.py
│   │   │       ├── scipy-1.15.3-cp310-cp310-win_amd64.whl
│   │   │       ├── six.py
│   │   │       ├── threadpoolctl.py
│   │   │       ├── txt2tags.py
│   │   │       └── typing_extensions.py
│   │   ├── Scripts
│   │   │   ├── accelerate-config.exe
│   │   │   ├── accelerate-estimate-memory.exe
│   │   │   ├── accelerate-launch.exe
│   │   │   ├── accelerate-merge-weights.exe
│   │   │   ├── accelerate.exe
│   │   │   ├── activate
│   │   │   ├── activate.bat
│   │   │   ├── Activate.ps1
│   │   │   ├── cffi-gen-src.exe
│   │   │   ├── datasets-cli.exe
│   │   │   ├── deactivate.bat
│   │   │   ├── debugpy-adapter.exe
│   │   │   ├── debugpy.exe
│   │   │   ├── diffusers-cli.exe
│   │   │   ├── f2py.exe
│   │   │   ├── fonttools.exe
│   │   │   ├── get_gprof
│   │   │   ├── get_objgraph
│   │   │   ├── gguf-convert-endian.exe
│   │   │   ├── gguf-dump.exe
│   │   │   ├── gguf-editor-gui.exe
│   │   │   ├── gguf-new-metadata.exe
│   │   │   ├── gguf-set-metadata.exe
│   │   │   ├── hf.exe
│   │   │   ├── httpx.exe
│   │   │   ├── huggingface-cli.exe
│   │   │   ├── idna.exe
│   │   │   ├── ipython.exe
│   │   │   ├── ipython3.exe
│   │   │   ├── isympy.exe
│   │   │   ├── jlpm.exe
│   │   │   ├── jsonpointer
│   │   │   ├── jsonschema.exe
│   │   │   ├── jupyter-builder.exe
│   │   │   ├── jupyter-console.exe
│   │   │   ├── jupyter-dejavu.exe
│   │   │   ├── jupyter-events.exe
│   │   │   ├── jupyter-execute.exe
│   │   │   ├── jupyter-kernel.exe
│   │   │   ├── jupyter-kernelspec.exe
│   │   │   ├── jupyter-lab.exe
│   │   │   ├── jupyter-labextension.exe
│   │   │   ├── jupyter-labhub.exe
│   │   │   ├── jupyter-migrate.exe
│   │   │   ├── jupyter-nbconvert.exe
│   │   │   ├── jupyter-notebook.exe
│   │   │   ├── jupyter-run.exe
│   │   │   ├── jupyter-server.exe
│   │   │   ├── jupyter-troubleshoot.exe
│   │   │   ├── jupyter-trust.exe
│   │   │   ├── jupyter.exe
│   │   │   ├── markdown-it.exe
│   │   │   ├── mistral_common.exe
│   │   │   ├── mistune.exe
│   │   │   ├── normalizer.exe
│   │   │   ├── numpy-config.exe
│   │   │   ├── pip.exe
│   │   │   ├── pip3.10.exe
│   │   │   ├── pip3.exe
│   │   │   ├── pybabel.exe
│   │   │   ├── pyftmerge.exe
│   │   │   ├── pyftsubset.exe
│   │   │   ├── pygmentize.exe
│   │   │   ├── pyjson5.exe
│   │   │   ├── python.exe
│   │   │   ├── pythonw.exe
│   │   │   ├── send2trash.exe
│   │   │   ├── tiny-agents.exe
│   │   │   ├── torchfrtrace.exe
│   │   │   ├── torchrun.exe
│   │   │   ├── tqdm.exe
│   │   │   ├── transformers.exe
│   │   │   ├── trl.exe
│   │   │   ├── ttx.exe
│   │   │   ├── txt2tags.exe
│   │   │   ├── typer.exe
│   │   │   ├── undill
│   │   │   ├── unsloth.exe
│   │   │   ├── wheel.exe
│   │   │   └── wsdump.exe
│   │   ├── share
│   │   │   ├── applications
│   │   │   │   ├── jupyter-notebook.desktop
│   │   │   │   └── jupyterlab.desktop
│   │   │   ├── icons
│   │   │   │   └── hicolor
│   │   │   │       └── scalable
│   │   │   ├── jupyter
│   │   │   │   ├── kernels
│   │   │   │   │   └── python3
│   │   │   │   ├── lab
│   │   │   │   │   ├── schemas
│   │   │   │   │   ├── static
│   │   │   │   │   └── themes
│   │   │   │   ├── labextensions
│   │   │   │   │   ├── @jupyter-notebook
│   │   │   │   │   ├── @jupyter-widgets
│   │   │   │   │   └── jupyterlab_pygments
│   │   │   │   ├── nbconvert
│   │   │   │   │   └── templates
│   │   │   │   └── nbextensions
│   │   │   │       └── jupyter-js-widgets
│   │   │   └── man
│   │   │       └── man1
│   │   │           ├── ipython.1
│   │   │           ├── isympy.1
│   │   │           └── ttx.1
│   │   └── pyvenv.cfg
│   ├── 01_prepare_dataset.py
│   ├── 02_train_lora_unsloth.py
│   ├── 03_evaluate.py
│   ├── aes_finetuning_pipeline.ipynb
│   ├── cleaned_dataset.csv
│   ├── export_aes_dataset.py
│   ├── fine_tuning_llama3.2-instruct.ipynb
│   ├── Modelfile
│   ├── test.jsonl
│   ├── train.jsonl
│   └── val.jsonl
├── static
│   └── admin
│       └── js
│           └── nim_nip_toggle.js
├── docker-compose.yml
├── Dockerfile
├── DockerFile.finetune
├── manage.py
├── netstat
├── README.md
└── requirements.txt
```


## Fitur Utama Backend

*   *** Auth & User Management**:
    *   Menggunakan **JWT Authentication** (`djangorestframework-simplejwt`).
    *   Login fleksibel: Bisa menggunakan **Username**, **NIM** (Mahasiswa), atau **NIP** (Dosen).
    *   **Single-Device Login Enforcement**: Mengunci sesi login hanya untuk satu perangkat aktif. Jika login di perangkat baru, token perangkat lama otomatis di-blacklist.
*   *** Zero-Tolerance Proctoring**:
    *   API Heartbeat berkala (setiap 15 detik) untuk mendeteksi status keaktifan mahasiswa.
    *   Pencatatan log pelanggaran kecurangan: *Membuka Tab Baru*, *Window Blur (Pindah Aplikasi)*, dan *Keluar Layar Fullscreen*.
    *   **Auto-Lock Akun**: Jika ada pelanggaran, ujian langsung dihentikan dan akun mahasiswa otomatis terkunci (`is_exam_locked=True`).
*   *** AI Automatic Grading**:
    *   Integrasi Celery worker ke Ollama secara lokal.
    *   Melakukan kalkulasi nilai esai (Skala 0, 5, 10) dengan pencocokan kata kunci dan referensi jawaban.
    *   Menyediakan feedback/alasan penilaian dalam Bahasa Indonesia secara otomatis.
*   *** Reporting & Export**:
    *   Export rekap nilai kelas berupa spreadsheet Excel (`.xlsx`) dengan styling tabel kustom.
    *   Export hasil ujian individu mahasiswa berupa dokumen PDF (`.pdf`) lengkap dengan detail penilaian per nomor soal.
*   *** Admin Customization**:
    *   Akses Django Admin eksklusif dibatasi hanya untuk **Superuser** (Administrator IT).
    *   Dynamic admin fields: Field NIM/NIP/Kelas otomatis bersembunyi secara dinamis (menggunakan vanilla JS) tergantung role user yang dipilih.

---

## Environment Variables (`.env`)

Buat file `.env` di direktori utama proyek (sudah diabaikan oleh `.gitignore` agar aman):

```env
DB_NAME=essay_db
DB_USER=essay_user
DB_PASSWORD=essay_password_2024
SECRET_KEY=-dsyr&i0j71@25_ffscbo1y4y#fl$@1^(v93c--n)9h5y&bi+b
DEBUG=1
REDIS_URL=redis://redis:6379/0
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=llama3.2:3b
```

---

## Panduan Instalasi & Run (Docker)

Pastikan **Docker Desktop** sudah berjalan di komputer Anda sebelum memulai.

### 1. Bangun & Jalankan Container
```bash
docker compose down -v  # Bersihkan cache volume lama jika ada conflict
docker compose up --build -d
```

### 2. Jalankan Migrasi Database
```bash
docker compose exec web python manage.py migrate
```

### 3. Buat Akun Superuser/Dosen Utama
```bash
docker compose exec web python manage.py createsuperuser
```
> Masukkan username yang tidak mengandung spasi (misalnya: `admin.dosen` atau `mustainul.abdi`).

### 4. Pull Model LLM (Hanya Sekali)
Unduh model Llama 3.2 ke dalam service Ollama Anda atau menyesuikan dengan kemampuan komputasi perangkat anda:
```bash
docker compose exec ollama ollama pull llama3.2:3b
```

### 5. Salin Static Files (Untuk Django Admin)
```bash
docker compose exec web python manage.py collectstatic --noinput
```

Sistem backend kini dapat diakses di: **`http://localhost:8443/api/v1/`** atau menggunakan IP LAN Anda (contoh: **`http://192.168.110.47:8443/api/v1/`**).

---

## Endpoint API Utama

### Authentication (`/api/v1/auth/`)
*   `POST /login/` : Login pengguna (dapat JWT Access & Refresh Token).
*   `POST /logout/` : Logout pengguna (memasukkan refresh token ke blacklist).
*   `GET /profile/` : Mengambil data diri profile pengguna yang aktif.
*   `GET /mahasiswa/` : (Dosen Only) Mengambil seluruh daftar mahasiswa.
*   `POST /mahasiswa/import/` : (Dosen Only) Upload data mahasiswa via Excel (.xlsx).
*   `GET /mahasiswa/export-kartu/` : (Dosen Only) Download PDF kartu login mahasiswa.
*   `POST /mahasiswa/<pk>/unlock/` : (Dosen Only) Membuka kembali akun mahasiswa yang terkunci karena pelanggaran.

### Ujian & Mata Kuliah (`/api/v1/ujian/`)
*   `GET | POST /mata-kuliah/` : Kelola daftar mata kuliah aktif.
*   `GET | POST /` : Kelola daftar ujian.
*   `POST /<pk>/aktivasi/` : Mengubah status ujian.
*   `GET /<pk>/monitor/` : Live monitor progress dan status pelanggaran peserta ujian.
*   `GET /tersedia/` : (Mahasiswa Only) Menampilkan ujian aktif yang siap dikerjakan berdasarkan kelas mahasiswa.

### Ujian & Submissions (`/api/v1/submission/`)
*   `POST /mulai/<ujian_pk>/` : Memulai sesi ujian baru atau melanjutkan sesi sebelumnya.
*   `POST /save-jawaban/` : Auto-save jawaban per nomor soal secara periodik.
*   `POST /submit/<sesi_pk>/` : Mengakhiri ujian dan mentrigger AI automatic grading di background.
*   `GET /hasil/<sesi_pk>/` : Memantau (polling) hasil kelulusan / nilai yang dinilai oleh AI.

### Proctoring/Pengawasan (`/api/v1/proctoring/`)
*   `POST /heartbeat/` : Mengirimkan signal keaktifan browser setiap 15 detik (mengembalikan sisa waktu ujian).
*   `POST /pelanggaran/` : Mencatat pelanggaran kecurangan (window blur / new tab / exit fullscreen) sekaligus langsung mengunci akun siswa.

### Laporan Nilai (`/api/v1/laporan/`)
*   `GET /nilai/<ujian_pk>/` : Ringkasan tabel nilai seluruh siswa kelas.
*   `GET /export/excel/<ujian_pk>/?kelas=<nama_kelas>` : Download berkas Excel styled nilai ujian mahasiswa.
*   `GET /export/pdf/<sesi_pk>/` : Download transkrip penilaian PDF individu mahasiswa (isi teks jawaban, skor, dan alasan penilaian dari AI).
