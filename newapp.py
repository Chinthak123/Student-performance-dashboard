import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


@st.cache_data
def load_data():
    df = pd.read_csv('StudentsPerformance.csv')
    df['total_score'] = df['math score'] + df['reading score'] + df['writing score']
    df['at_risk'] = (df['math score'] < 50) | (df['reading score'] < 50) | (df['writing score'] < 50)
    return df

df = load_data()

st.title("🎓 Student Performance Dashboard")


with st.expander("🔍 Key Analysis Findings"):
    st.write(f"**1. Parental Education:** Higher parental education levels correlate with higher average scores.")
    st.write(f"**2. Test Prep:** Students who complete the course score significantly higher.")
    st.write(f"**3. Correlation:** There is a very strong positive correlation (r > 0.8) between reading, writing, and math.")
    st.write(f"**4. Gender Performance:** Females typically outperform in reading/writing; males in math.")
    st.write(f"**5. Score Distribution:** Total scores follow a near-normal distribution centered around 200/300.")


c1, c2 = st.columns(2)
with c1:
    fig1 = px.box(df, x='parental level of education', y='total_score', title="Scores by Parental Education")
    st.plotly_chart(fig1, use_container_width=True)
with c2:
    fig2 = px.bar(df.groupby('test preparation course')['total_score'].mean().reset_index(), 
                  x='test preparation course', y='total_score', title="Avg Score: Test Prep Comparison")
    st.plotly_chart(fig2, use_container_width=True)

c3, c4 = st.columns(2)
with c3:
    fig3 = px.imshow(df[['math score', 'reading score', 'writing score']].corr(), text_auto=True, title="Correlation Heatmap")
    st.plotly_chart(fig3, use_container_width=True)
with c4:
    fig4 = px.bar(df.groupby('gender')[['math score', 'reading score', 'writing score']].mean().reset_index().melt(id_vars='gender'), 
                  x='variable', y='value', color='gender', barmode='group', title="Gender vs Subject Performance")
    st.plotly_chart(fig4, use_container_width=True)

c5, c6 = st.columns(2)
with c5:
    fig5 = px.histogram(df, x='total_score', nbins=20, title="Total Score Distribution")
    st.plotly_chart(fig5, use_container_width=True)
with c6:
    fig6 = px.scatter(df, x='reading score', y='math score', color='gender', title="Reading vs Math Scores")
    st.plotly_chart(fig6, use_container_width=True)


st.subheader("⚠️ At-Risk Student Segmentation")
at_risk_count = df['at_risk'].sum()
st.metric("Total At-Risk Students", at_risk_count)
st.write("At-risk students are defined as those scoring below 50 in any subject. These students often lack test preparation course completion.")