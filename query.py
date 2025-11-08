import rdflib
import textwrap

# --- Helper Function for Pretty Printing ---
def print_query_results(query_title, query_question, query_string, results):
    """
    Formats and prints the results of a SPARQL query in a clean, readable way.
    """
    print("=" * 80)
    print(f"| Query: {query_title}")
    print(f"|  Q: \"{query_question}\"")
    print("-" * 80)
    
    results_list = list(results)
    
    if not results_list:
        print(textwrap.indent("No results found.", "  -> "))
    else:
        for row in results_list:
            # Format each variable in the row
            parts = []
            for item in row:
                if isinstance(item, rdflib.Literal):
                    parts.append(f"\"{item}\"") # Print literals in quotes
                else:
                    parts.append(str(item))
            row_str = ", ".join(parts)
            print(textwrap.indent(row_str, "  -> "))
    
    print("\n") # Add a newline for spacing

# --- Main Query Script ---
def run_queries():
    g = rdflib.Graph()
    
    # --- STEP 1: CONFIGURATION ---
    ontology_file = "plant-disease-ontology.ttl" # This is correct
    
    IRI = "http://www.semanticweb.org/knuckles/ontologies/2025/10/plant-disease-ontology#"
    
    # --- END OF CONFIGURATION ---

    try:
        g.parse(ontology_file, format="turtle")
    except Exception as e:
        print(f"ERROR: Could not parse '{ontology_file}'. Details: {e}")
        return

    # Define and bind your namespace.
    NS = rdflib.Namespace(IRI)
    g.bind("", NS) # Bind to the default prefix ":"
    g.bind("rdfs", rdflib.RDFS)
    g.bind("owl", rdflib.OWL)
    
    print(f"Successfully loaded Knowledge Graph from '{ontology_file}'")
    print(f"Total Triples in Graph: {len(g)}\n")

    # --- Query 1  ---
    title1 = "Symptoms by Disease"
    question1 = "What are the symptoms of 'Late Blight'?"
    query1_string = """
        SELECT ?symptom_label
        WHERE {
            :LateBlight :hasSymptom ?symptom_iri .
            ?symptom_iri rdfs:label ?symptom_label .
        }
    """
    results1 = g.query(query1_string)
    print_query_results(title1, question1, query1_string, results1)

    # --- Query 2 ---
    title2 = "Diseases by Host Plant"
    question2 = "Which diseases affect the ':Tomato' plant?"
    query2_string = """
        SELECT ?disease_label
        WHERE {
            ?disease_iri a/rdfs:subClassOf* :Disease ;
                         :affectsHost :Tomato ;
                         rdfs:label ?disease_label .
        }
    """
    results2 = g.query(query2_string)
    print_query_results(title2, question2, query2_string, results2)
    
    # --- Query 3 ---
    title3 = "Diseases by Pathogen Type (Fungus)"
    question3 = "What diseases in the knowledge base are caused by a Fungus?"
    query3_string = """
        SELECT ?disease_label ?fungus_label
        WHERE {
            ?fungus_iri a :Fungus ;
                        rdfs:label ?fungus_label .
            ?disease_iri :isCausedBy ?fungus_iri ;
                         rdfs:label ?disease_label .
        }
    """
    results3 = g.query(query3_string)
    print_query_results(title3, question3, query3_string, results3)

    # --- Query 4 ---
    title4 = "Symptom to Disease (Diagnostic)"
    question4 = "I see 'Wilting'. What diseases could this be?"
    query4_string = """
        SELECT ?disease_label
        WHERE {
            ?symptom_iri rdfs:label "Wilting" .
            ?disease_iri :hasSymptom ?symptom_iri ;
                         rdfs:label ?disease_label .
        }
    """
    results4 = g.query(query4_string)
    print_query_results(title4, question4, query4_string, results4)

# --- Main execution ---
if __name__ == "__main__":
    run_queries()
