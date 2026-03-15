import subprocess
import time



def semigroup(t):
    return [ (t + "_semigroup_assoc", "semigroupAssociativity" + t.capitalize()) ]
def monoid(t):
    return [ (t + "_monoid_rightid", "monoidRightIdentity" + t.capitalize()), 
             (t + "_monoid_leftid", "monoidLeftIdentity" + t.capitalize()),
             (t + "_monoid_concatenation", "monoidConcatenation" + t.capitalize()) ]
def functor(t):
    return [ (t + "_functor_id", "fmapId" + t.capitalize()), 
             (t + "_functor_composition", "fmapComposition" + t.capitalize()) ]
def app(t):
    return [ (t + "_app_id", "appIdentity" + t.capitalize()), 
             (t + "_app_composition", "appComposition" + t.capitalize()),
             (t + "_app_homomorphism", "appHomomorphism" + t.capitalize()),
             (t + "_app_interchange", "appHomomorphism" + t.capitalize())]
def monad(t):
    return [ (t + "_monad_leftid", "monadLeftIdentity" + t.capitalize()), 
             (t + "_monad_rightid", "monadRightIdentity" + t.capitalize()),
             (t + "_monad_assoc", "monadAssociativity" + t.capitalize())]

list_props = semigroup("list") + monoid("list") + functor("list") + app("list") + monad("list")
maybe_props = semigroup("maybe") + monoid("maybe") + functor("maybe") + app("maybe") + monad("maybe")
nonempty_props = semigroup("nonempty") + functor("nonempty") + functor("nonempty") + monad("nonempty")
tree_props = functor("tree")
function_props = semigroup("function") + functor("function") + monad("function")
pair_props = semigroup("pair") + functor("pair") + monad("pair")
state_props = functor("state") + monad("state")
props = list_props + maybe_props + nonempty_props + tree_props + function_props + pair_props + state_props

results = {}

for (prop, out_name) in props:
    print(["sbt"] + ["run -b " + prop])
    start_time = 0
    end_time = 0
    succeeded = False
    neither = True
    res = subprocess.Popen(["sbt"] + ["run -b " + prop], stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(res.stdout.readline, ""):
        if "running propel.check" in stdout_line:
            start_time = time.perf_counter()
        if "Check failed" in stdout_line:
            end_time = time.perf_counter()
            neither = False
        if "Check successful" in stdout_line:
            end_time = time.perf_counter()
            succeeded = True
            neither = False
    if neither:
        raise RuntimeError("No result")
    
    res.stdout.close()

    run_time = end_time - start_time
    results[out_name] = str(run_time) if succeeded else "-"
    print(prop)
    print(results[out_name])

print("results")
for pr in results:
    print(pr + " & " + results[pr])