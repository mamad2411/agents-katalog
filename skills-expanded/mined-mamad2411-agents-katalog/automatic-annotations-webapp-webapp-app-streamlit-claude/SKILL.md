# Steramlit UIデザイン

## ページ一覧

|ファイル名|概要|
|---|---|
|main.py|データセットを選択する（DATASET_IDをセッションに保持）|
|pages/1_Scene_Selection.py|シーンを選択する（SCENE_TOKENをセッションに保持）|
|pages/2_Detection2D.py|Grounding DINOを用いて、与えたラベルの2D bounding boxを検出|
|pages/3_Instance_Tracking.py|2_Detection2D.pyで検出したボックスをプロンプトとして与えたSAM2を用いて、各インスタンスのマスクとtrack_idを取得|
|pages/4_Depth_Boxfitting.py|Depth-Anything-3でカメラ画像から推論した点群とLiDAR点群をミックスして、3_Instance_Tracking.pyで検出したマスク範囲にprojectionして3D bounding boxを割り当てる|

## 各ページの仕様
### main.py
- 最初に表示される画面であり、ここでデータセットを選択する
- データセット一覧を、各種統計情報（シーン数、サンプル数、アノテーション数等）と一緒に画面上部にテーブル表示する
- テーブルのチェックボックスをチェックして「このデータセットを使う」ボタンをクリックすると、データセット選択（DATASET_ID）がセッションに保存されて他の画面に遷移しても維持される
- データセット選択がセッションに保存されると「シーン選択へ進む」ボタンが表示され、クリックすると1_Scene_Selection.pyの画面に遷移する

### 1_Scene_Selection.py
- シーンを選択するための画面
- データセット選択（DATASET_ID）がセッションに保存されていない場合、「先にデータセットを選択してください」という文字とmain.pyに遷移する「データセット選択へ」ボタンのみ表示し、以降のUIを表示しない
- 選択中のデータセット内のScene一覧を、各種統計情報（logから取得したlocation、開始時刻等）と一緒に画面上部にテーブル表示する
- テーブルにはシーン内の「紐づくsample_annotationが1個以上あるsampleの数 / 全sample数」を「アノテーション済」列として表示し、このパーセンテージを「進捗」列としてバー表示する。また進捗が100%なら完了、0%なら未着手、それ以外なら実施中と表示する「状態」列も追加する
- テーブルのチェックボックスをクリックすると、右下に各sampleの位置をwaypointとして地図上にPlotlyで表示する（sampleに紐づくLIDAR_TOPのego-poseを使用）
- テーブルのチェックボックスをチェックして「このシーンでアノテーションを開始」ボタンをクリックすると、当該シーンを選択選択（SCENE_TOKENがセッションに保存されて他の画面に遷移しても維持される）して2_Detection2D.py画面に遷移する

### 2_Detection2D.py
- Grounding DINOを用いて、与えたラベルの2Dバウンディングボックスを検出する画面。アルゴリズム詳細については`webapp/inference/CLAUDE.md`の`Detection2D`参照
- 画面上部はparam_col, map_colで左右に分割
- param_col上部のexpanderに以下の推論パラメータを選択するUIを設置
    - Sample Interval: 推論を実施するsampleの間隔。number_inputで選択
    - Score Threshold: 検出したバウンディングボックスのscore閾値にかける倍率。sliderで選択。実際に適用する閾値はカテゴリグループごとに異なるDET2D_DEFAULT_SCORE_THRESHOLDSにここで選択した倍率を掛けたものとなる
    - NMS Threshold: 検出したバウンディングボックスでNMSを実施するIoUの閾値にかける倍率。sliderで選択。実際に適用する閾値は、同クラス間のbox結合はカテゴリグループごとに異なる`Settings.DET2D_NMS_SAME_CLASS_IOUS`にここで選択した倍率を掛けたもの、別クラス間のbox結合は`Settings.DET2D_NMS_CROSS_CLASS_IOU`にここで選択した倍率を掛けたものとなる
    - Re-Classification Crop Margin: SigLIP2での再判定に使用する切り出し画像作成時に、元来のGroundingDINO検出バウンディングボックスから拡張する領域の割合
- param_col中央上部の枠付きcontainerに推論を実施する「Run Inference」ボタンを設置。ボタンを押すと上で選択したパラメータを渡して推論を実行する`POST /detection2d/jobs`リクエストがInferenceサーバーに送信され、定期的に`GET /detection2d/jobs/{job_id}`リクエストでポーリングして得られた進捗が表示される
- ポーリングで推論完了を検知（完了を2回検知して2回保存するのを防ぐため保存済み`params_id`をsession_stateに持っておく）したら、以下の要件を満たすよう結果をDBの`detection_2d_params`、`detection_2ds`テーブルに保存する
    - 推論が完了したら、即時に自動保存（人間がボタンを押したら保存すると、せっかく時間をかけて推論した結果が消えうるため）。ただし過去に手作業で修正したバウンディングボックスがあれば優先して使用するため、保存前に以下処理をsample_data_tokenごと（Sample＆カメラごと）に実行
        - `detection_2ds`テーブル内の`manually_modified=True`のレコード（マニュアル編集済ボックス）と、推論した全ボックスに対してIoUを計算して貪欲マッチング（1つの手修正ボックスが複数の推論ボックスとマッチして同じ手修正ボックスが複製されるのを防ぐため）を実施
        - マッチングしたIoUが閾値（`Settings.DET2D_MANUAL_REPLACE_IOU`）以上のボックスがあれば、マッチングした推論ボックスをマッチングしたマニュアル編集済ボックスに置き換える
        - マッチしなかったマニュアル編集済ボックスは、そのまま推論結果に追加する
        - 手修正にはボックスの削除処理も存在するが、今回の置き換えロジックのスコープ外（推論ボックスを削除する処理は実施しない）
    - 保存は上書きではなくレコード追加として行う。保存時に同じ(dataset_id, scene_token)の`instance_tracking_2d_params`から参照されていない`detection_2d_params`レコードが`Settings.DET2D_MAX_RUNS_PER_SCENE`件以上あれば、最も古いレコードを削除する（CASCADEで紐づく`detection_2ds`テーブルのレコードも削除される）
    - 保存は1トランザクションで一括追加（キャンセル時の後始末が楽になる）
- `detection_2d_params`テーブルに当該Sceneの`status='succeeded'`のレコードがあれば（推論を成功裏に実施・保存済みであれば）、param_col中央下部のexpanderにラジオボタン付きでレコード一覧をリスト表示する。選択中のレコードが参照している`instance_tracking_2d_params`テーブルのレコードがあれば、参照されている旨を表示する。リストの下には「このrunを表示」と「削除」ボタンを設置し、押すと以下のように動作する
    - 「このrunを表示」ボタン: 押すと後述のview_colで表示される「推論バウンディングボックス」をラジオボタン選択したレコードのものに切り替える
    - 「削除」ボタン: 押すと選択した`detection_2d_params`テーブルのレコードと、CASCADEで紐づく`detection_2ds`テーブルのレコードも削除される。CASCADEで紐づくInstance Tracking、Depth Boxfittng関係のレコードも削除されるが、この場合は削除前に警告を出す
- param_col最下部に、表示するsampleを選択するためのSelect Sampleスライダを設置。このスライダはSample Intervalパラメータの間隔に基づく選択したサンプルのリスト（推論もこのサンプルのみ実施される）をselect_sliderで表示する
- map_colに各sampleの位置をwaypointとして地図上にPlotlyで表示し、上記Select Sampleスライダで選択中のsampleの位置を強調表示する（選択中sample強調表示以外は1_Scene_Selection.py画面で使用したコンポーネントと同じものを使用する）
- 画面下部は、view_col, opt_colで左右に分割する。view_colは各カメラの画像と「推論バウンディングボックス」（定義は後述）を表示（labelごとに色分け）し、opt_colに配置した表示条件を指定するための以下ウィジェットに基づき、以下のように表示を変える
    - Show boxesチェックボックス: チェックすると画像にバウンディングボックスを重ねて表示し、チェックしていないと画像のみを表示する
    - Compare with GT チェックボックス: チェックの有無に応じて以下のように表示を変える
        - チェックしていない場合: 2列3行で6カメラを表示し推論バウンディングボックスを重ねる
        - チェックしている場合: 2列6行で行ごとに各カメラ画像を2個ずつ表示し、左側の画像にはGround truthのバウンディングボックスを、右側の画像には推論バウンディングボックスを重ねて表示
    - Min scoreスライダ: 選択したscoreを超えたバウンディングボックスのみを表示
    - チェックボックス付きlabel凡例: チェックしているlabelのバウンディングボックスのみを表示。この凡例は選択中のsampleのバウンディングボックスに存在するlabelのみ表示。一括チェックする「全て」ボタンと、一括チェック解除する「解除」ボタンも設置
    - Box textラジオボタン: 画像上でバウンディングボックスの上に表示する文字の種類（文字色はバウンディングボックスの色と一致）を指定する。以下の選択肢を持つ
        - None: 何も表示しない
        - Detection Label: GroundingDINOの推論結果を表示（SubLabelから`LABEL_TO_SUBLABEL`で逆引きして得られる）
        - SubLabel: 実際にGroundingDINOのプロンプトに渡したサブラベルを表示
        - Re-Classification: SigLIP2で再判定して得られたラベルを表示
        - Label: 最終的なラベルを表示（SigLIP2で再判定して得られたラベルを`RE_CLASSIFICATION_CANDIDATES`で参照して得られる）
        - Score: スコアを表示（小数点以下2桁まで表示）
- view_colに表示する推論バウンディングボックスは、以下のように決める
    - （現在のセッションでの）推論実施前: `detection_2d_params`テーブルの`status='succeeded'`のレコードのうち`started_at`が最新のもの。`status='succeeded'`のレコードがなければバウンディングボックスを表示しなし
    - 推論実施後: 推論結果のバウンディングボックス（基本的には推論実施前と同様に`detection_2d_params`テーブルの`status='succeeded'`のレコードのうち`started_at`が最新のものになるはず）
    - 表示対象の変更方法: 手動操作を行わなければ上記のように表示対象が決まるが、前述のparam_col中央下部のexpanderで「このrunを表示」ボタンを押すと、ラジオボタンで選択した`detection_2d_params`テーブルのレコードのものに切り替わる

### 3_Instance_Tracking.py
- SAM2を用いて、与えたラベルの2Dバウンディングボックスを検出する画面。アルゴリズム詳細については`webapp/inference/CLAUDE.md`の`Instance Tracking`参照
- 画面上部はparam_col, map_colで左右に分割
- param_col上部のexpanderに以下の推論パラメータを選択するUIを設置
    - Box Prompt: プロンプトとして渡すDetection2Dのボックス。`detection_2d_params`テーブル内の`status='succeeded'`のレコードをラジオボタン付きでリスト表示する。デフォルトでは`started_at`が最新のものを選択
    - Sweeps per Sample: トラッキングに使用する画像のSampleあたりsweep数（1ならキーフレームのみを使用。デフォルト値`Settings.DEFAULT_TRACKING_NUM_SWEEPS`）。`Settings.SWEEPS_PER_SAMPLE`を上限としたnumber_input
    - IoU Threshold: track_idのブロック間引き継ぎに使用するインスタンス同士のHungarian algorithmによるIoUマッチング後のIoU閾値。デフォルト値`Settings.DEFAULT_TRACKING_IOU_THRESHOLD`
    - IoU Method: 上記IoUマッチングで使用するIoUの計算方法を、外径バウンディングボックス同士のIoUにするか、Mask IoUにするかを選択。”Box”, “Mask”のselectboxで良さそう。デフォルトは”Box”
    - IoU Label Match: 上記IoUマッチング時にラベルまたはカテゴリグループの一致も考慮するかを指定するSelectbox。以下の選択肢を持つ
        - Label: ラベルが一致する場合のみマッチング対象とする
        - Category Group: カテゴリグループが一致する場合のみマッチング対象とする
        - None: ラベル・カテゴリグループの一致に関わらずマッチング対象とする
    - Track ID Inheritance: IoUマッチングに使用する手法を指定するSelectbox。以下の選択肢を持つ（両手法の詳細は`webapp/inference/CLAUDE.md`参照）
        - continuous_id: 最初のフレームにボックスプロンプト（Detection2Dの結果）を与えて時間順方向（Forward方向）にトラッキングし、得られた最後のフレームのインスタンスと、次のブロックの最初のフレームにボックスプロンプトを与えて得られたインスタンスをIoUマッチング
        - forward_backward_matching: 最初のフレームにボックスプロンプトを与えたForward方向トラッキングと、最後のフレームにボックスプロンプトを与えた時間逆方向（Backward方向）トラッキングを実施し、両トラッキングの各インスタンスの全フレームでの時空間IoUマッチングを実施
- 推論container: Detection2D画面と同様（「Run Inference」ボタンを押すと推論実行リクエストがInferenceサーバーに送信され、定期的にポーリングして得られた進捗が表示される）
- param_col中央上部の枠付きcontainerに推論を実施する「Run Inference」ボタンを設置。ボタンを押すと上で選択したパラメータを渡して推論を実行する`POST /instance-tracking/jobs`リクエストがInferenceサーバーに送信され、定期的に`GET /instance-tracking/jobs/{job_id}`リクエストでポーリングして得られた進捗が表示される
- ポーリングで推論完了を検知（完了を2回検知して2回保存するのを防ぐため保存済み`params_id`をsession_stateに持っておく）したら、以下の要件を満たすよう結果をDBの`instance_tracking_2d_params`、`instance_tracking_2ds`テーブルに保存する
    - 推論が完了したら、即時に自動保存
        - `detection_2ds`テーブル内の`manually_modified=True`のレコード（マニュアル編集済ボックス）と、推論した全ボックスに対してIoUを計算して貪欲マッチング（1つの手修正ボックスが複数の推論ボックスとマッチして同じ手修正ボックスが複製されるのを防ぐため）を実施
        - マッチングしたIoUが閾値（`Settings.DET2D_MANUAL_REPLACE_IOU`）以上のボックスがあれば、マッチングした推論ボックスをマッチングしたマニュアル編集済ボックスに置き換える
        - マッチしなかったマニュアル編集済ボックスは、そのまま推論結果に追加する
        - 手修正にはボックスの削除処理も存在するが、今回の置き換えロジックのスコープ外（推論ボックスを削除する処理は実施しない）
    - 保存は上書きではなくレコード追加として行う。保存時に同じ(dataset_id, scene_token)の`depth_estimation_params`から参照されていない`instance_tracking_2d_params`レコードが`Settings.TRACKING_MAX_RUNS_PER_SCENE`件以上あれば、最も古いレコードを削除する（CASCADEで紐づく`instance_tracking_2ds`テーブルのレコードも削除される）
    - 保存は1トランザクションで一括追加（キャンセル時の後始末が楽になる）
- `instance_tracking_2d_params`テーブルに当該Sceneの`status='succeeded'`のレコードがあれば（推論を成功裏に実施・保存済みであれば）、param_col中央下部のexpanderにラジオボタン付きでレコード一覧をリスト表示する。選択中のレコードが参照している`depth_estimation_params`テーブルのレコードがあれば、参照されている旨を表示する。リストの下には「このrunを表示」と「削除」ボタンを設置し、押すと以下のように動作する
    - 「このrunを表示」ボタン: 押すと後述のview_colで表示される「推論バウンディングボックス」をラジオボタン選択したレコードのものに切り替える
    - 「削除」ボタン: 押すと選択した`instance_tracking_2d_params`テーブルのレコードと、CASCADEで紐づく`instance_tracking_2ds`テーブルのレコードも削除される。CASCADEで紐づくDepth Boxfittng関係のレコードも削除されるが、この場合は削除前に警告を出す
- param_col最下部に、表示するsampleを選択するためのSelect Sampleスライダを設置。Detection2D画面と異なり、全てのSampleを選択できるようにする（トラッキングはIntervalの間のフレームにも実行されるため）。Sample選択だとキーフレーム以外は選択できなくなるが、これで特に問題ない（キーフレーム以外のフレームは推論のトラッキング伝播には使用するが、結果自体は使用しないため表示できなくとも良い）
- map_colにはDetection2D画面と同様、各sampleの位置をwaypointとして地図上にPlotlyで表示し、上記Select Sampleスライダで選択中のsampleの位置を強調表示する
- 画面下部は、view_col, opt_colで左右に分割する。view_colは各カメラの画像とインスタンスマスクを表示（labelごとに色分け）し、opt_colに配置した表示条件を指定するための以下ウィジェットに基づき、以下のように表示を変える
    - Compare propagation: track_idの引き継ぎ時のインスタンス同士のマッチングを確認するモード。チェックの有無により以下のように表示が変わる
        - チェックしていない場合: 2列3行で6カメラを表示し推論マスクやバウンディングボックス等を重ねる。Track ID Inheritance="forward_backward_matching"のとき、各インスタンスの表示マスクは以下のように決める
            - そのインスタンスがBackward・Forwardどちらかの伝播にのみ存在（マッチング成立せず）: 伝播が存在するインスタンスマスクをそのまま表示
            - そのインスタンスがBackward・Forward両方の伝播に存在（マッチング成立）: 最終的に採用するマスクの決め方と同じく、そのフレームからプロンプトボックスが近い方のインスタンスマスクを表示（例. ForwardがSample4から、BackwardがSample8から伝播している場合、Sample4〜6ではForwardのマスクを、Sample7〜8ではBackwardのマスクを表示）
        - チェックしている場合: 2列6行で行ごとに各カメラ画像を2個ずつ表示し、track_idの引き継ぎに使用する2種類のインスタンスマスクを比較する。Track ID Inheritanceに応じて以下のように表示が変わる
            - continuous_idのとき: 左側の画像には前のSample Intervalから伝播したマスクを表示する（Show boxesでPromptを選択している場合、ボックスは表示しない）。右側の画像には今回のSample Intervalで推論したマスクを表示する（Show boxesラジオボタンでPromptを選択している場合、プロンプトボックスは表示する）
            - forward_backward_matchingのとき: 左側の画像にはForward方向トラッキングで伝播されたマスクを、右側の画像にはBackward方向トラッキングで伝播されたマスクを表示する。プロンプトボックスを与えるフレーム（Sample Interval間隔で存在）は2つのブロックに重複して所属するため、2種類のBackwardおよびForwardマスクが存在することとなるが、左側の画像（Forward）にはプロンプトを与えて得られたマスク（前のブロックからForward伝播されたマスクではない）を、右側の画像（Backward）にはそのブロックの最後のフレームからBackward伝播されてきたマスク（プロントを与えて得られたマスクではない）を表示する。Show boxesラジオボタンでPromptを選択している場合、左側の画像（Forward）にプロンプトボックスを表示する。
    - Show boxesラジオボタン: 画像上でのバウンディングボックスの表示方法を指定する。以下の選択肢を持つ（デフォルトはPrompt）
        - Prompt: プロンプトとして与えたbox（Sample Intervalで選ばれたSampleでしか表示されないことになる）
        - Instance: インスタンスマスクの外接矩形（全Sampleにおいて表示される）
        - None: バウンディングボックスを表示しない
    - Colorラジオボタン: マスクとバウンディングボックスの表示色の決め方選択。以下の選択肢を持つ（デフォルトはLabel）
        - Label: ラベルで色分け
        - Track ID: Track IDで色分け
    - Instance textラジオボタン: 画像上でインスタンスの上に表示する文字の種類を指定する。以下の選択肢を持つ（デフォルトはTrack ID）
        - None: 何も表示しない
        - Label: ラベル文字を表示（文字色はマスクの色と一致）
        - Track ID: Track IDを表示（文字色はマスクの色と一致）
    - 凡例のリスト表示: Colorで選択した色に応じてチェックボックス付き凡例をリスト表示（レイアウトはDetection2D画面のものを踏襲）

### 4_Depth_Boxfitting.py
- Depth-Anything-3を用いてカメラ画像から深度推定してDepth点群を取得し、それを各インスタンスマスクに投影して（LiDAR点群があればこれも混合して）インスタンスごとの点群を作成し、3Dバウンディングボックスを当てはめる画面。アルゴリズム詳細については`webapp/inference/CLAUDE.md`の`Depth Boxfitting`参照
- 画面上部はparam_col, map_colで左右に分割
- param_col上部のexpanderに推論パラメータを選択するUIを設置し、以下のタブに分ける
    - Instance Tracking（これのみタブではなくラジオボタン）: 入力として使用するInstance Trackingの結果。`instance_tracking_2d_params`テーブル内の`status='succeeded'`のレコードをラジオボタン付きでリスト表示する。デフォルトでは`started_at`が最新のものを選択
    - Generalタブ: Depth/LiDAR点群両方の処理に適用するパラメータ
        - Use LiDAR: LiDAR点群を使用するかどうかを指定するチェックボックス
        - Dilation: インスタンスマスクのクロージング処理の膨張カーネルサイズ
        - Erosion: インスタンスマスクのクロージング処理の
    - Depth Estimation: 深度推定で得られたDepth点群のノイズ除去に使用するパラメータ
        - ROR: ノイズ除去の1段階目の処理であるROR（Radius Outlier Removal）に使用するパラメータ
            - nb_points: nb_pointsパラメータ（指定した半径の球内に存在しなければならない最小の点の個数）
            - radius: radiusパラメータ（注目する点を中心とした球の半径）
        - DBSCAN: ノイズ除去の2段階目の処理であるDBSCANに使用するパラメータ
            - eps: epsパラメータ（近傍とみなす半径）
            - min_samples: min_samplesパラメータ（コア点とみなすために半径eps内に存在しなければならない最小のデータ点数）
    - LiDAR Pointcloud: LiDAR点群の結合・ノイズ除去・Depth点群とのに使用するパラメータ
        - LiDAR Sweeps: キーフレームあたりで結合するLiDAR点群のsweep数
        - Min LiDAR Points: インスタンス点群として使用するための点数のしきい値（これを下回ったインスタンスはDepth点群のみ使用する）
        - ROR: ノイズ除去の1段階目の処理であるROR（Radius Outlier Removal）に使用するパラメータ
            - nb_points: nb_pointsパラメータ（指定した半径の球内に存在しなければならない最小の点の個数）
            - radius: radiusパラメータ（注目する点を中心とした球の半径）
        - DBSCAN: ノイズ除去の2段階目の処理であるDBSCANに使用するパラメータ
            - eps: epsパラメータ（近傍とみなす半径）
            - min_samples: min_samplesパラメータ（コア点とみなすために半径eps内に存在しなければならない最小のデータ点数）
    - Box Fitting: 3Dバウンディングボックスのインスタンスごと点群へのフィッティングに使用するパラメータ
        - Method: 3Dバウンディングボックスのフィッティングに使用するアルゴリズム。以下の選択肢をもつ
            - convex_hull_moa: [こちらの論文](https://arxiv.org/abs/2302.01034)の手法。以下のパラメータを指定可能
                - angle_step_deg: 最もフィットするyaw角度を探索するステップ
                - z_percentile: 高さの下限と上限として採用するパーセンタイル
    - Inter-cam Merge: 複数カメラ間での同一インスタンス結合に使用するパラメータ
        - 

- 推論container: Detection2D画面と同様（「Run Inference」ボタンを押すと推論実行リクエストがInferenceサーバーに送信され、定期的にポーリングして得られた進捗が表示される）
- param_col中央上部の枠付きcontainerに推論を実施する「Run Inference」ボタンを設置。ボタンを押すと上で選択したパラメータを渡して推論を実行する`POST /instance-tracking/jobs`リクエストがInferenceサーバーに送信され、定期的に`GET /instance-tracking/jobs/{job_id}`リクエストでポーリングして得られた進捗が表示される
- ポーリングで推論完了を検知（完了を2回検知して2回保存するのを防ぐため保存済み`params_id`をsession_stateに持っておく）したら、以下の要件を満たすよう結果をDBの`instance_tracking_2d_params`、`instance_tracking_2ds`テーブルに保存する
    - 推論が完了したら、即時に自動保存
        - `detection_2ds`テーブル内の`manually_modified=True`のレコード（マニュアル編集済ボックス）と、推論した全ボックスに対してIoUを計算して貪欲マッチング（1つの手修正ボックスが複数の推論ボックスとマッチして同じ手修正ボックスが複製されるのを防ぐため）を実施
        - マッチングしたIoUが閾値（`Settings.DET2D_MANUAL_REPLACE_IOU`）以上のボックスがあれば、マッチングした推論ボックスをマッチングしたマニュアル編集済ボックスに置き換える
        - マッチしなかったマニュアル編集済ボックスは、そのまま推論結果に追加する
        - 手修正にはボックスの削除処理も存在するが、今回の置き換えロジックのスコープ外（推論ボックスを削除する処理は実施しない）
    - 保存は上書きではなくレコード追加として行う。保存時に同じ(dataset_id, scene_token)の`depth_estimation_params`から参照されていない`instance_tracking_2d_params`レコードが`Settings.TRACKING_MAX_RUNS_PER_SCENE`件以上あれば、最も古いレコードを削除する（CASCADEで紐づく`instance_tracking_2ds`テーブルのレコードも削除される）
    - 保存は1トランザクションで一括追加（キャンセル時の後始末が楽になる）
- `instance_tracking_2d_params`テーブルに当該Sceneの`status='succeeded'`のレコードがあれば（推論を成功裏に実施・保存済みであれば）、param_col中央下部のexpanderにラジオボタン付きでレコード一覧をリスト表示する。選択中のレコードが参照している`depth_estimation_params`テーブルのレコードがあれば、参照されている旨を表示する。リストの下には「このrunを表示」と「削除」ボタンを設置し、押すと以下のように動作する
    - 「このrunを表示」ボタン: 押すと後述のview_colで表示される「推論バウンディングボックス」をラジオボタン選択したレコードのものに切り替える
    - 「削除」ボタン: 押すと選択した`instance_tracking_2d_params`テーブルのレコードと、CASCADEで紐づく`instance_tracking_2ds`テーブルのレコードも削除される。CASCADEで紐づくDepth Boxfittng関係のレコードも削除されるが、この場合は削除前に警告を出す
- param_col最下部に、表示するsampleを選択するためのSelect Sampleスライダを設置。Detection2D画面と異なり、全てのSampleを選択できるようにする（トラッキングはIntervalの間のフレームにも実行されるため）。Sample選択だとキーフレーム以外は選択できなくなるが、これで特に問題ない（キーフレーム以外のフレームは推論のトラッキング伝播には使用するが、結果自体は使用しないため表示できなくとも良い）
- map_colにはDetection2D画面と同様、各sampleの位置をwaypointとして地図上にPlotlyで表示し、上記Select Sampleスライダで選択中のsampleの位置を強調表示する
- 画面下部は、view_col, opt_colで左右に分割する。view_colは各カメラの画像とインスタンスマスクを表示（labelごとに色分け）し、opt_colに配置した表示条件を指定するための以下ウィジェットに基づき、以下のように表示を変える
    - Compare propagation: track_idの引き継ぎ時のインスタンス同士のマッチングを確認するモード。チェックの有無により以下のように表示が変わる
        - チェックしていない場合: 2列3行で6カメラを表示し推論マスクやバウンディングボックス等を重ねる。Track ID Inheritance="forward_backward_matching"のとき、各インスタンスの表示マスクは以下のように決める
            - そのインスタンスがBackward・Forwardどちらかの伝播にのみ存在（マッチング成立せず）: 伝播が存在するインスタンスマスクをそのまま表示
            - そのインスタンスがBackward・Forward両方の伝播に存在（マッチング成立）: 最終的に採用するマスクの決め方と同じく、そのフレームからプロンプトボックスが近い方のインスタンスマスクを表示（例. ForwardがSample4から、BackwardがSample8から伝播している場合、Sample4〜6ではForwardのマスクを、Sample7〜8ではBackwardのマスクを表示）
        - チェックしている場合: 2列6行で行ごとに各カメラ画像を2個ずつ表示し、track_idの引き継ぎに使用する2種類のインスタンスマスクを比較する。Track ID Inheritanceに応じて以下のように表示が変わる
            - continuous_idのとき: 左側の画像には前のSample Intervalから伝播したマスクを表示する（Show boxesでPromptを選択している場合、ボックスは表示しない）。右側の画像には今回のSample Intervalで推論したマスクを表示する（Show boxesラジオボタンでPromptを選択している場合、プロンプトボックスは表示する）
            - forward_backward_matchingのとき: 左側の画像にはForward方向トラッキングで伝播されたマスクを、右側の画像にはBackward方向トラッキングで伝播されたマスクを表示する。プロンプトボックスを与えるフレーム（Sample Interval間隔で存在）は2つのブロックに重複して所属するため、2種類のBackwardおよびForwardマスクが存在することとなるが、左側の画像（Forward）にはプロンプトを与えて得られたマスク（前のブロックからForward伝播されたマスクではない）を、右側の画像（Backward）にはそのブロックの最後のフレームからBackward伝播されてきたマスク（プロントを与えて得られたマスクではない）を表示する。Show boxesラジオボタンでPromptを選択している場合、左側の画像（Forward）にプロンプトボックスを表示する。
    - Show boxesラジオボタン: 画像上でのバウンディングボックスの表示方法を指定する。以下の選択肢を持つ（デフォルトはPrompt）
        - Prompt: プロンプトとして与えたbox（Sample Intervalで選ばれたSampleでしか表示されないことになる）
        - Instance: インスタンスマスクの外接矩形（全Sampleにおいて表示される）
        - None: バウンディングボックスを表示しない
    - Colorラジオボタン: マスクとバウンディングボックスの表示色の決め方選択。以下の選択肢を持つ（デフォルトはLabel）
        - Label: ラベルで色分け
        - Track ID: Track IDで色分け
    - Instance textラジオボタン: 画像上でインスタンスの上に表示する文字の種類を指定する。以下の選択肢を持つ（デフォルトはTrack ID）
        - None: 何も表示しない
        - Label: ラベル文字を表示（文字色はマスクの色と一致）
        - Track ID: Track IDを表示（文字色はマスクの色と一致）
    - 凡例のリスト表示: Colorで選択した色に応じてチェックボックス付き凡例をリスト表示（レイアウトはDetection2D画面のものを踏襲）
