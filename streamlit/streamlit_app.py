import streamlit as st
from name_ticker_module import find_similar_names_and_tickers
from bing_search_module import bing_search_news
from polygon_module import get_stock_price_history
from calendar_module import get_first_last_days
from cohere_rerank_module import rerank_search_results
from financial_bert_module import predict_monthly_stock_price_change_rate
import matplotlib.pyplot as plt

# Streamlit app layout
st.title('Stock Analysis and Prediction')

# Company Name Search
user_input = st.text_input("Enter a company name", "Tesla")
if user_input:
    search_results = find_similar_names_and_tickers(user_input)
    option = st.selectbox('Choose a company:', search_results)
    name, ticker = option

    calculate_button = st.button('Calculate')
    if calculate_button:
        this_month_articles = bing_search_news(name)
        articles_content = [article['description'] for article in this_month_articles]

        reranked_articles_content = rerank_search_results(name, articles_content, 5)
        st.subheader("Cohere Reranked Articles:")
        for article in reranked_articles_content:
            st.write("-", article)

        concatenated_articles_content = " ".join(reranked_articles_content)
        monthly_stock_price_change_rate = predict_monthly_stock_price_change_rate(concatenated_articles_content)

        past_month_first_day_str, current_month_last_day_str, year_month_labels = get_first_last_days()
        stock_price_history = get_stock_price_history(ticker, past_month_first_day_str, current_month_last_day_str)
        predicted_next_month_stock_price = stock_price_history[-1] * (1 + monthly_stock_price_change_rate)
        stock_price_history.append(predicted_next_month_stock_price)

        # Plotting the data
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(year_month_labels[:-1], stock_price_history[:-1], label='History', marker='o')
        ax.plot(year_month_labels[-2:], stock_price_history[-2:], label='Prediction', color='red', marker='o')

        # Adding labels and title
        ax.set_xlabel('Year-Month')
        ax.set_ylabel('Stock Price')
        ax.set_title('Stock Price History and Prediction')
        plt.xticks(rotation=45)

        # Adding legend
        ax.legend()

        # Show the plot in Streamlit
        st.pyplot(fig)