// convex/messages.ts
import { query, mutation, internalMutation } from "./_generated/server";
import { internal } from "./_generated/api";
import { v } from "convex/values";
import { paginationOptsValidator } from "convex/server";

export const listMessages = query({
  args: { paginationOpts : paginationOptsValidator},
  handler: async (ctx, args) => {
    return await ctx.db.query("messages").order("desc").paginate(args.paginationOpts);
  },
});

export const send = mutation({
  args: { author: v.string(), message: v.string() },
  handler: async (ctx, { author, message }) => {
    // Send a new message.
    await ctx.db.insert("messages", { author, message });
  },
});

export const deleteEmptyMessages = mutation({
  args: {}, // We don't need arguments here
  handler: async (ctx) => {
    // Find all messages with empty messages
    const emptyMessages = await ctx.db.query("messages").filter((q) => q.eq(q.field("message"), "")); // Use await to fetch results

    // Option 1: Collect all empty messages
    const emptyMessagesData = await emptyMessages.collect(); // Uncomment if you need all messages

    // Option 2: Take the first n empty messages (replace n with your desired limit)
    //const emptyMessagesData = await emptyMessages.take(10); // Uncomment if you only need a limited number

    // Delete each empty message
    for (const message of emptyMessagesData) {
      await ctx.scheduler.runAfter(5000, internal.messages.internalDelete, { messageId: message._id });
    }
  },
});


export const internalDelete = internalMutation({
  args: {
    messageId: v.id("messages"),
  },
  handler: async (ctx, args) => {
    await ctx.db.delete(args.messageId);
  },
});