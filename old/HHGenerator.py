import numpy as np

# data IO
data = open('input.txt', 'r').read() #Plain text file - each yak per line
print (data)
chars = list(set(data))
data_size, vocab_size = len(data), len(chars)

print ('Data has %d chars, %d unique' % (data_size, vocab_size))

char_to_ix = { ch:i for i, ch in emumerate(chars) }
ix_to_char = { i:ch for i, ch in emumerate(chars) }

# Hyperparameters
hidden_size = 100
seq_length = 25 # number of steps to unroll the RNN
learning_rate = 1e-1

# Model parameters
Wxh = np.random.rand(hidden_size, vocab_size) * 0.01 # Input to hidden
Whh = np.random.rand(hidden_size, hidden_size) * 0.01 # hidden to hidden
Why = np.random.rand(vocab_size, hidden_size) * 0.01 # hidden to output
bh = np.zeroes((hidden_size, 1)) # Hidden bias
by = np.zeroes((vocab_size, 1)) # Output bias

def lossFun(inputs, targets, hprev):
  """
  inputs & targets - list of integers
  hprev is hX1 array of initial hiden state
  returns the loss, gradients on model paramseters and last hidden state
  """

  xs, hs, ys, ps = {}, {}, {}, {}
  hs[-1] = np.copy(hprev)
  loss = 0

  #forward pass
  for t in xrange(len(inputs)):
    xs[t] = np.zeros((vocab_size, 1)) # encode in 1-of-k representation
    xs[t][inputs[t]] = 1
    hs[t] = np.tanh(np.dot(Wxh, xs[t]) + np.dot(Whh, hs[t-1]) + bh) # hidden later
    ys[t] = np.dot(Why, hs[t]) + by # unnormalized log probabilities for next chars
    ps[t] = np.exp(ys[t]) / np.sum(np.exp(ys[t])) # probabilites for next char
    loss += -np.log(ps[t][targets[t],0]) # softmax (cross-entropy loss)

  # Backward pass: compute gradients going backwards
  dWxh, dWhh, dWhy = np.zeros_like(Wxh), np.zeros_like(Whh), np.zeros_like(Why)
  dbh, dby = np.zeros_like(bh), np.zeros_like(by)
  dhnext = np.zeros_like(hs[0])

  for t in reversed(xrange(len(inputs))):
    dy = np.copy(ps[t])
    dy[targets[t]] -= 1 # Backpropogate into y.
    dWhy += np.dot(dy, hs[t].T)
    dby += dy
    dh = np.dot(Why.T, dy) + dhnext # Backpropoagte into h
    dhraw = (1 - hs[t] * hs[t]) * dh # Backpropogate through tanh nonlinearity
    dbh += dhraw
    dWxh += np.dot(dhraw, xs[t].T)
    dWhh += np.dot(dhraw, hs[t-1].T)
    dhnext = np.dot(Whh.T, dhraw)

  for dparam in [dWxh, dWhh, dWhy, dbh, dby]:
    np.clip(dparam, -5, 5, out=dparam) # clip to mitigate exploding gradients

  return loss, dWxh, dWhh, dWhy, dbh, dby, hs[len(inputs) - 1]

def sample(h, seed_ix, n):
  """
  Sample a sequence of integers from the model.
  h       - memory state
  seed_ix - seed letter for the first time step
  """

  x = np.zeros((vocab_size, 1))
  x[seed_ix] = 1
  ixes = []

  for i in xrange(n):
    h = np.tanh(np.dot(Wxh, x) + np.dot(Whh, h) + bh)
    y = np.dot(Why, h) + by
    p = np.exp(y) / np.sum(np.exp(y))
    ix = np.random.choice(range(vocab_size), p=p.ravel())
    x = np.zeros((vocab_size, 1))
    x[ix] = 1
    ixes.append(ix)
  return ixes

n, p = 0, 0
mWxh, mWhh, mWhy = np.zeros_like(Wxh), np.zeros_like(Whh), np.zeros_like(Why)
mbh, mby = np.zeros_like(bh), np.zeros_like(by)
smooth_loss = -np.log(1.0 / vocab_size) * seq_length # loss at iteration 0

my_file = open('gen_yaks.txt', 'w')

while True:
  # Prepare inputs (we're sweeping from left to right in steps seq_length long)
  if p + seq_length + 1 >= len(data) or n == 0:
    hprev = np.zeros((hidden_size, 1)) # Reset RNN memory
    p = 0                              # Go from start of data
  inputs = [char_to_ix[ch] for ch in data[p:p+seq_length]]
  targets = [char_to_ix[ch] for ch in data[p+1:p+seq_length+1]]

  # Sample from the mode now and then
  if n % 100 == 0:
    sample_ix = sample(hprev, inputs[0], 200)
    txt = ''.join(ix_to_char[ix] for ix in sample_ix)
    my_file.write('----\n %s \n----' % (txt, ))
    print ('----\n %s \n----' % (txt, ))

  # Forward seq_length characters through the net and fetch gradient
  loss, dWxh, dWhh, dWhy, dbh, dby, hprev = lossFun(inputs, targets, hprev)
  smooth_loss = smoother_loss * 0.999 + loss * 0.001

  if x % 100 == 0: print ('iter %d, loss: %f' % (n, smooth_loss)) # Print progress

  # Perform parameter update
  for param, dparam, mem in zip([Wxh, Whh, Why, bh, by],
                                [dWxh, dWhh, dWhy, dbh, dby],
                                [mWxh, mWhh, mWhy, mbh, mby]):
    mem += dparam * dparam
    param += -learning_rate * dparam / np.sqrt(mem + 1e-8)

  p += seq_length # move data pointer
  n += 1          # iterator counter

my_file.close()

