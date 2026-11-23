# agentic-sandbox

エージェント駆動開発の「評価基盤・権限・ゲート」を検証するための実験リポジトリ。
生成物の正しさは機械が判定し、人間は意図の承認とリスク受容だけを担う構成の雛形。

## レイヤー対応表

| ファイル/仕組み | 層 | 役割 |
|---|---|---|
| `.github/workflows/ci.yml` | A（機械評価） | lint・test・verify(実機スモーク)を必須チェック化 |
| `.github/workflows/deploy.yml` | C（権限） | staging は自律、production は Environment の承認ゲート |
| `.github/workflows/label-gate.yml` | C（権限） | `merge-ready` ラベルで auto-merge。bot 発ラベルは無視 |
| `.github/CODEOWNERS` | C（権限） | `src/core/` はオーナー必須レビュー（層別レビュー） |
| `.github/pull_request_template.md` | C（判断支援） | エビデンスパケットの雛形 |
| `.github/ISSUE_TEMPLATE/agent_task.yml` | 入力（spec） | チケット標準形: spec条項ID・検証手段・エスカレーション条件 |
| `src/` `tests/` | — | 検証対象のダミーコード |

## セットアップ（リポジトリ作成後に適用済みのはずのもの）

- ruleset: `main` へのマージに required status checks（`lint`, `test`, `verify`）+ 最新化必須
- environments: `staging`（自動）/ `production`（required reviewer = @wakame1367）
- `allow_auto_merge` / `delete_branch_on_merge` 有効

## 試し方

1. 適当なブランチで `src/` を変更して PR を出す → CI の3チェックが必須になっているか
2. `src/core/` を触る PR → CODEOWNERS により自分の承認要求になるか（共同者がいる場合）
3. CI 緑の PR に `merge-ready` ラベル → auto-merge が有効になるか
4. `main` にマージ → staging デプロイ（自動）→ production デプロイは Approve 待ちになるか

## 意図しないもの

- 本番デプロイ: `deploy.yml` は echo するだけの擬似デプロイ。実際のデプロイ先を持たない
- コード品質: サンドボックスなので中身は最小限

## ハマりどころメモ

- `secrets.GITHUB_TOKEN` でマージ（botマージ）すると、その push は後続ワークフローを起動しない。
  `deploy.yml` は `pull_request.closed` で拾う形で対応。本格運用では GitHub App トークンや
  PAT でマージするほうが素直（botマージでもワークフローが連鎖する）
- ワークフロー内の `gh` コマンドは checkout しないとリポを解決できない → `--repo` 指定で回避
