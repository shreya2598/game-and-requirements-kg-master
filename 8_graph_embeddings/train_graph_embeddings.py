import numpy as np
import pandas as pd
import ampligraph
from ampligraph.datasets import load_from_rdf
from ampligraph.evaluation import train_test_split_no_unseen
from ampligraph.latent_features import ComplEx
import tensorflow as tf
from ampligraph.evaluation import evaluate_performance
from ampligraph.utils import save_model, restore_model
from ampligraph.evaluation import mr_score, mrr_score, hits_at_n_score

if __name__ == "__main__":
    graph_file = "sample_Game_KG.nt"
    out_embeddings_file = "Game_KGE_model.pkl"
    embedding_dims = 100
    num_epochs = 300


    X = load_from_rdf('.', graph_file, rdf_format='nt', data_home='.')
    test_size = int(0.05 * X.shape[0])
    X_train, X_test = train_test_split_no_unseen(X, test_size=test_size)

    print('Train set size: ', X_train.shape)
    print('Test set size: ', X_test.shape)

    model = ComplEx(batches_count=100,
                    seed=0,
                    epochs=num_epochs,
                    k=embedding_dims,
                    eta=5,
                    optimizer='adam',
                    optimizer_params={'lr': 1e-3},
                    loss='multiclass_nll',
                    regularizer='LP',
                    regularizer_params={'p': 3, 'lambda': 1e-5},
                    verbose=True)

    positives_filter = X
    tf.logging.set_verbosity(tf.logging.ERROR)

    print("Model training started...")
    model.fit(X_train, early_stopping=False)

    print("Save the model...")
    save_model(model, model_name_path=out_embeddings_file)

    print("Evaluating the model...")
    ranks = evaluate_performance(X_test,
                                 model=model,
                                 filter_triples=positives_filter,
                                 use_default_protocol=True,
                                 verbose=True)
    mrr = mrr_score(ranks)
    print("MRR: %.2f" % (mrr))

    hits_10 = hits_at_n_score(ranks, n=10)
    print("Hits@10: %.2f" % (hits_10))
    hits_3 = hits_at_n_score(ranks, n=3)
    print("Hits@3: %.2f" % (hits_3))
    hits_1 = hits_at_n_score(ranks, n=1)
    print("Hits@1: %.2f" % (hits_1))