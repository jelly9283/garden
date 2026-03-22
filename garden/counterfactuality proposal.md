for a theory T and a sentence we want to consider S where T |- not S, we can still evaluate truth values of a statement A in T + S in some way, like this:
- P_c(T + S, A) = P_c(T + S |- A) / (P_c(T + S |- A) + P_c(T + S |- not A))
where P_c(T + S |- A) is the probability that a randomly sampled program generates a valid proof of T + S |- A, 0 if not found

[[info, Notes on logical priors from the MIRI workshop — LessWrong|someone has implemented this already]], although with a somewhat unrelated extension, particularly about a distribution on potentially-inconsistent theories, but now that i considered it i think it's a good extension.

related: [[Mathematics]], [[operationalizing FDT]]