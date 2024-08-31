import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

def connect_mysql():
    """Establish a connection to the MySQL server using SQLAlchemy."""
    try:
        engine = create_engine("mysql+mysqlconnector://root:selva@localhost:3306/redbus_details")
        return engine
    except SQLAlchemyError as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None

def fetch_data_from_db(query=None):
    """Fetch data from the MySQL database using SQLAlchemy."""
    engine = connect_mysql()
    if engine:
        try:
            df = pd.read_sql(query, engine) if query else pd.read_sql("SELECT * FROM redbus_details", engine)
            return df
        except SQLAlchemyError as e:
            st.error(f"Error fetching data: {e}")
            return None
    return None

def main():
    """Main function to run the Streamlit app."""
    st.sidebar.title("Main Menu")

    if st.sidebar.button("Home"):
        st.session_state.clear()

    st.sidebar.button("Select the Bus", on_click=lambda: st.session_state.update({'page': 'bus_details'}))

    # Home Page Layout
    if 'page' not in st.session_state:
        st.title("Welcome to the RedBus Details App!")
        st.markdown("<h3 style='color: blue;'>Find Your Bus Details Easily</h3>", unsafe_allow_html=True)
        st.write(
            "This app allows you to search for bus details, including available seats, types, and routes. "
            "Please use the menu on the left to get started."
        )

        # Center content
        st.write("")
        if st.button("Get Started", key="start"):
            st.session_state.update({'page': 'bus_details'})

        st.write(
            "### Instructions:\n"
            "- **Select the Bus:** Choose a route and find the available buses.\n"
            "- **Filter Options:** Narrow down your search by seat type, price, and more."
        )
        return

    # Fetch all bus details for filtering
    bus_df = fetch_data_from_db()

    if bus_df is not None and not bus_df.empty:
        # Filtering options
        routes = bus_df['route_name'].unique().tolist()
        selected_route = st.selectbox("Select the Route", routes)
        
        # Filter the DataFrame based on the selected route
        route_filtered_df = bus_df[bus_df['route_name'] == selected_route]
        
        bus_names = route_filtered_df['bus_name'].unique().tolist()
        selected_bus_name = st.selectbox("Select the Bus", bus_names)
        
        # Filter again based on the selected bus name
        bus_filtered_df = route_filtered_df[route_filtered_df['bus_name'] == selected_bus_name]
        
        if not bus_filtered_df.empty:
            # Display available seat types
            seat_types = bus_filtered_df['bus_type'].unique().tolist()
            selected_seat_type = st.selectbox("Available Seat Types", seat_types)
            
            # Display available seats
            available_seats = bus_filtered_df['seats_available'].unique().tolist()
            st.write(f"Available Seats: {available_seats[0]}")
            
            # Optionally, filter based on seat type if needed
            seat_filtered_df = bus_filtered_df[bus_filtered_df['bus_type'] == selected_seat_type]
            
            # Display the filtered bus details
            st.write(f"### Bus Details for {selected_bus_name} on Route {selected_route}")
            st.dataframe(seat_filtered_df)
        else:
            st.write("No buses available for the selected bus name.")
    else:
        st.write("No data available to display.")

if __name__ == "__main__":
    main()
