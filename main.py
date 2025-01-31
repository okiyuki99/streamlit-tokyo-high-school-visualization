import streamlit as st
import pandas as pd
import plotly.express as px

# タイトルの設定
st.title("東京都立高校 入学試験応募状況の推移 (2022-2024)")
st.write("過去3年間の都立高校の応募状況を可視化しています。")

# データの読み込み
@st.cache_data
def load_data():
    # カラム名を統一
    columns = ['区市町村名', '学校名', '募集人員', '最終応募人員', '最終応募倍率']
    
    # 各年度のデータを読み込み、カラム名を統一
    df_2022 = pd.read_csv('data/2022_tokyo_high_school_Entrance_examination_application_status.csv', names=columns, header=0)
    df_2023 = pd.read_csv('data/2023_tokyo_high_school_Entrance_examination_application_status.csv', names=columns, header=0)
    df_2024 = pd.read_csv('data/2024_tokyo_high_school_Entrance_examination_application_status.csv', names=columns, header=0)
    
    # 年度の列を追加
    df_2022['年度'] = 2022
    df_2023['年度'] = 2023
    df_2024['年度'] = 2024
    
    # データを結合
    df = pd.concat([df_2022, df_2023, df_2024])
    return df

# データの読み込み
df = load_data()

# サイドバーに検索フィルター追加
st.sidebar.header('フィルター')
selected_district = st.sidebar.multiselect(
    '区市町村名を選択',
    options=sorted(df['区市町村名'].unique()),
    default=[]
)

# データのフィルタリング
if selected_district:
    filtered_df = df[df['区市町村名'].isin(selected_district)]
else:
    filtered_df = df

# 応募倍率の推移グラフ
st.subheader('応募倍率の推移')
fig = px.line(filtered_df, 
              x='年度', 
              y='最終応募倍率',
              color='学校名',
              title='高校別応募倍率の推移',
              labels={'最終応募倍率': '応募倍率', '年度': '年度'},
              markers=True)
fig.update_layout(height=600)
fig.update_xaxes(tickformat="d")
st.plotly_chart(fig, use_container_width=True)

# 応募人数の推移グラフ
st.subheader('応募人数の推移')
fig_applicants = px.line(filtered_df, 
                        x='年度', 
                        y='最終応募人員',
                        color='学校名',
                        title='高校別応募人数の推移',
                        labels={'最終応募人員': '応募人数', '年度': '年度'},
                        markers=True)
fig_applicants.update_layout(height=600)
fig_applicants.update_xaxes(tickformat="d")
st.plotly_chart(fig_applicants, use_container_width=True)

# データテーブルの表示
st.subheader('詳細データ')
st.dataframe(filtered_df.sort_values(['学校名', '年度']))
