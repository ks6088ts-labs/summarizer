[![test](https://github.com/ks6088ts-labs/summarizer/workflows/test/badge.svg)](https://github.com/ks6088ts-labs/summarizer/actions/workflows/test.yml)
[![release](https://github.com/ks6088ts-labs/summarizer/workflows/release/badge.svg)](https://github.com/ks6088ts-labs/summarizer/actions/workflows/release.yml)

# summarizer

## How to use

```bash
# Install dependencies
make install-deps

# Run tests
make ci-test

# Run server
make server

# Call API from another terminal
curl 'http://localhost:8888/azure_openai/invoke' \
  -H 'Content-Type: application/json' \
  --data-raw '{"input":{"topic":"「セロトニン」は気分や覚醒リズムに関わる脳内の神経伝達物質です。セロトニンの不足は不安や意欲低下を引き起こす原因の一つとなっていますが、その詳しい仕組みまでは分かっていませんでした。しかし量子科学技術研究開発機構（QST）は今回、サルを実験対象にセロトニン不足で意欲低下が生じる仕組みを調査。その結果、サルの脳内セロトニンレベルを下げると、ご褒美を期待することでやる気が高まる「報酬効果」が低下し、さらに課題クリアにかかるコストに敏感になり、行動したくないという「億劫感」が上昇することが判明しました。研究の詳細は、2024年1月1日付で科学雑誌『Plos Biology』に掲載されています。"},"config":{}}'

# Call API from browser
# access http://localhost:8888/azure_openai/playground/
```
