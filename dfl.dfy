/* Dutch National Flag
 * sort an array that has four different keys
 */

datatype Color = Orange | Red | White | Blue

// ordering of colors: Orange > Red > White > Blue
predicate Above(c: Color, d: Color)
{
  true // TODO
}

method sortFlag(a: array<Color>)
  modifies a // needed for arrays (since they are objects, not values such as sequences)
  ensures forall i,j | 0 <= i < j < a.Length :: Above(a[i], a[j])
  ensures multiset(a[..]) == multiset(old(a[..]))
{
  var N := a.Length;
  var r, w, u := 0, 0, N; // marks the red part, white part, unsorted part
  while //TODO
    // TODO
    invariant multiset(a[..]) == multiset(old(a[..]))
  {
    // TODO
  }
}

method TestColordering() {
  assert Above(Red, White);
  assert Above(White, Blue);
  assert Above(White, White);
  assert Above(Orange, Red);
  assert ! Above(Blue, Orange);
  assert ! Above(White, Red);
}
