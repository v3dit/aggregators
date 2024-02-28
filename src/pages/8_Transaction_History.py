# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore

# # Initialize Firebase Admin with your credentials
# cred = credentials.Certificate('firestore-test-8d0a8-firebase-adminsdk-he1cx-cedc3e03d3.json')
# firebase_admin.initialize_app(cred)

# # Create a Firestore client
# db = firestore.client()

# # Function to read a document from Firestore
# # def read_document(collection_name, document_id):
# #     doc_ref = db.collection(collection_name).document(document_id)
# #     doc = doc_ref.get()
# #     if doc.exists:
# #         print(f'Document data: {doc.to_dict()}')
# #     else:
# #         print('No such document!')

# def read_all_documents(collection_name):
#     collection_ref = db.collection(collection_name)
#     docs = collection_ref.stream()
#     print(docs)
#     docs1=[]
#     for doc in docs:
#         # print(f'{doc.id} => {doc.to_dict()}')
#         docs1.append(doc.to_dict())
#     return docs1

# # Example usage
# collection_name = 'Test'
# read_all_documents(collection_name)

# # Example usage
# # collection_name = 'Test'
# # document_id = 'your_document_id'
# # read_document(collection_name, document_id)
import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


# Initialize Firebase Admin with your credentials
if not firebase_admin._apps :
    cred = credentials.Certificate('v3dit/aggregators/src/pages/streamlit_data/firestore-test-8d0a8-firebase-adminsdk-he1cx-cedc3e03d3.json')
    firebase_admin.initialize_app(cred)
    
else:
    pass

# Create a Firestore client
db = firestore.client()

# Function to read all documents from a collection in Firestore
def read_all_documents(collection_name):
    collection_ref = db.collection(collection_name)
    docs = collection_ref.stream()
    docs_list = []
    for doc in docs:
        docs_list.append(doc.to_dict())
    return docs_list

# Example usage
collection_name = 'Test'
transactions = read_all_documents(collection_name)

# Streamlit app code
st.title("Transactions List")
st.write("#### Efficiently monitor your sales and analyze purchasing patterns. Whether you're managing a small business or exploring data insights, this tool streamlines the process of tracking transactions and understanding customer behavior.")
# Display transactions list
# if transactions:
#     for transaction in transactions:
#         st.write(transaction)
# else:
#     st.write("No transactions found.")
total_cost = 0
if transactions:
    total_items_sold = 0
    for transaction in transactions:
        total_item_cost = transaction['quantity'] * transaction['price']
        st.success(f"Item: {transaction['title']}  ,Quantity: {transaction['quantity']}  ,Price: ${transaction['price']}")
        total_cost += total_item_cost
        total_items_sold += transaction['quantity']
    st.write(f"## Total Cost of Cart: ${total_cost}")
    st.write(f"## Total Items Sold: {total_items_sold}")
else:
    st.write("No transactions found.")


