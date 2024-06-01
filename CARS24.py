import pandas as pd
import streamlit as st
import pickle

# Load the dataset
cars_df = pd.read_excel(r"CARS24_Car-Price-Prediction-App/cars24-car-price.xlsx")


# Page configuration
st.set_page_config(
    page_title="Cars24: Car Price Prediction",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar
st.sidebar.header("User Input Features")
st.sidebar.write(
    """
    This app predicts the price of used cars based on various features. Use the options below to input car details.
    """
)

# Main title and description
st.title("🚗 Cars24: Car Price Prediction")
st.markdown(
    """
    This app predicts the price of used cars based on various features such as fuel type, transmission type, engine power, number of seats, and seller type. Users can input these features through user-friendly dropdown menus and sliders. The prediction is made using a trained machine learning model, allowing users to quickly estimate the selling price of a car they are interested in. With an intuitive interface design and informative feedback messages, the app provides an efficient tool for car buyers and sellers to make informed decisions.
    """
)

# Display reference data
st.subheader("Reference Data")
st.dataframe(cars_df.head())

# Encoding dictionary for categorical variables
encode_dict = {
    "fuel_type": {'Diesel': 1, 'Petrol': 2, 'CNG': 3, 'LPG': 4, 'Electric': 5},
    "seller_type": {'Dealer': 1, 'Individual': 2, 'Trustmark Dealer': 3},
    "transmission_type": {'Manual': 1, 'Automatic': 2}
}

# Function to load the model and make predictions
def model_pred(fuel_type, transmission_type, engine, seats, seller_type):
    # Load the model
    with open(r"model.pkl", 'rb') as file:
        reg_model = pickle.load(file)

    # Encode categorical features
    try:
        fuel_type_encoded = encode_dict['fuel_type'][fuel_type]
        transmission_type_encoded = encode_dict['transmission_type'][transmission_type]
        seller_type_encoded = encode_dict['seller_type'][seller_type]
    except KeyError as e:
        st.error("Error: " + str(e) + " is not recognized.")
        return None

    # Create input features array
    input_features = [[engine, seats, fuel_type_encoded, seller_type_encoded, transmission_type_encoded]]

    # Predict price
    price = reg_model.predict(input_features)
    return price

# User input features
st.sidebar.subheader("Configure the car details:")

# Fuel type selection
fuel_type = st.sidebar.selectbox("Select the fuel type", ["Diesel", "Petrol", "CNG", "LPG", "Electric"])

# Engine power slider
engine = st.sidebar.slider("Set the Engine Power (in HP)", 500, 5000, step=100, value=1500)

# Transmission type selection
transmission_type = st.sidebar.radio("Select the transmission type", ["Manual", "Automatic"])

# Number of seats selection
seats = st.sidebar.selectbox("Enter the number of seats", [4, 5, 7, 9, 11])

# Seller type selection
seller_type = st.sidebar.radio("Select the seller type", ["Dealer", "Individual", "Trustmark Dealer"], index=0)

# Display user selections
st.sidebar.write("### You selected:")
st.sidebar.write("**Fuel type:**", fuel_type)
st.sidebar.write("**Engine power:**", engine, "HP")
st.sidebar.write("**Transmission type:**", transmission_type)
st.sidebar.write("**Number of seats:**", seats)
st.sidebar.write("**Seller type:**", seller_type)

# Predict button
if st.sidebar.button("Predict Price"):
    # Call model_pred function to get the prediction
    price = model_pred(fuel_type, transmission_type, engine, seats, seller_type)
    if price is not None:
        st.success(f"The predicted price of the car is: **${round(price[0], 2)}**")

# Footer with additional information
st.markdown(
    """
    ---
    **Disclaimer:** This prediction is based on historical data and a machine learning model. Actual prices may vary based on various factors not accounted for in this model.
    """
)
